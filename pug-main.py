"""
"""


# Imports
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import re
import argparse
from datetime import date
import os
import glob
import string

# Consts
LOCAL_PATH = "c:\\pug\\"
PERMISSIONS = ["write", "all"]
# Classes
class reader:
    """
    reader(date) -> reads the dates data and retians it for usages in the object / parmissions dict named
    Users 
    """
    def __init__(self, date = date.today().strftime("%d/%m/%Y")):
        self.date = date.replace("/", "-")
        self.dirs = []
        self.listdirs() # populates self.dirs
        self.permissions = []
        self.all_perms()

    def listdirs(self):
        """
        will list all the dirs in the pug location and populate the self.dirs
        """
        os.chdir(LOCAL_PATH + str(self.date))
        self.dirs = os.listdir()
    
    def all_perms(self):
        """
        will populate all the users and their acl using the acl_reader object
        """
        # runs on all the dirs as parameters for acl_reader
        for d in self.dirs:
            a = acl_read(d)
            a.endGoal['1'] = d.lower().replace(" ","")
            self.permissions.append(a.endGoal)

            
class object_display:
    """
    object_display(permissions, objectname) --> only permissions regarding the object
    permissins - reader.permissions
    objectname - name of object
    takes one object out of all the reader.permissions class and shows only relevent to it data
    """
    def __init__(self, permissions, objectname):
        self.permissions = permissions
        self.objectname = objectname
        self.endGoal = []
        self.beenthere = []
        self.object_perms(self.objectname)
    
    def object_perms(self, objectname):
        """
        takes the permissions and changes them to regard only the effected objects
        works by recurssion with this function on each object it finds
        """
        for o in self.permissions:
            if o["1"] == objectname:
                self.endGoal.append(o)
                for e in o:
                    if e not in self.beenthere:
                        self.beenthere.append(e)
                        self.object_perms(e)

class mapper:
    """
    mapper(reader) -> gets our own reader object
    allows us to eassily show all the data in a networkx model
    """
    def __init__(self, permissions):
        self.permissions = permissions # saves the permissions dict
        self.G = nx.DiGraph() # the graph to show in the end
        self.nodes = [] # list of all the nodes names
        self.node_num = 0
        self.node_dict = {}
        self.reverse_node_dict = {}
        self.make_node() # l
        self.make_edge()
        

    def make_node(self):
        """
        make_node --> makes all the nodes and files up the needed dict for the drwaing
        node_dict/ reverse_node_dict
        """
        for o in self.permissions:
            for e in o:
                if e not in self.nodes:
                    if not e == '1':
                        self.reverse_node_dict[self.node_num] = e
                        self.nodes.append(e)
                        self.node_dict[e] = self.node_num
                        self.G.add_node(self.node_num)
                        self.node_num += 1
                    else:
                        if o['1'] not in self.nodes:
                            self.reverse_node_dict[self.node_num] = o['1']
                            self.nodes.append(o['1'])
                            self.node_dict[o['1']] = self.node_num
                            self.G.add_node(self.node_num)
                            self.node_num += 1                        

    def make_edge(self):
        """
        makes all the edges of this mapper classs
        """
        for o in self.permissions:
            for e in o:
                if not e == "1":
                    self.G.add_edge(self.node_dict[e], self.node_dict[o['1']])

    def display(self):
        """
        shows the graph created in the mapper class
        """
        pos = nx.spring_layout(self.G)
        nx.draw(self.G,pos, labels=self.reverse_node_dict, with_labels = True)
        plt.show()
        
    def dijkstra_display(self, src, dst):
        """
        src - source name
        dst - destination name
        will display the shortest path between src and dst
        """
        G = self.G
        pos = nx.spring_layout(G)
        nx.draw(G ,pos, labels=self.reverse_node_dict, with_labels = True)
        # draw path in red
        path = nx.shortest_path(G,source= self.node_dict[src], target=self.node_dict[dst])
        if not path == []: 
            path_edges = zip(tuple(path),tuple(path[1:]))
            path_edges = set(path_edges)
            nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='r')
            nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color='r',width=10)
        else:
            print("there is no connection between the 2")
        plt.axis('equal')
        plt.show()


class acl_read:
    """
    acl_read(path) -> reads the data in a directory and maps a object and who has rights on him
    all data is saved in the self.endGoal dict (endgoal = {})
    """
    def __init__(self, path):
        self.objects = [] # the object with the permissions in self.permissions
        self.permissions = [] # the permissions of object in self.object[i]
        self.endGoal = {} # the dict of user : permissions
        self.path = path # path to the object directoy
        self.fillup()

    def fillup(self):
        """
        fillup() -> will fill up the object list and the permissions so a objects[i] and permissions[i] match
        on the object
        """
        path = self.path    
        os.chdir((path))
        path = glob.glob('./*.txt')
        f = open(path[0], "r")
        acl = f.read()
        acl = acl.replace('\x00',"")
        acl = acl.split("\n")
        f.close()
        b = False
        # runs on all lines to find the object name and permissions
        for line in acl:
            if ("ActiveDirectoryRights :" in line):
                if any(p in (line.split(":")[1]).lower() for p in PERMISSIONS):
                    self.permissions.append((line.split(":")[1]).lower())
                    b = True
                else:
                    b = False
            elif bool(re.match("IdentityReference", line)) and b:
                self.objects.append((line.split(":")[1]).lower().replace("\\","-").replace(" ", ""))
        self.object_dict()
    
    def object_dict(self):
        """
        creates the endgoal
        """
        count = 0
        for o in self.objects:
            self.endGoal[o] = self.permissions[count].split(",")
        os.chdir("..\\")

class compare():
    """
    r1 - permissions of date1
    r2 - permissions of date2
    compares 2 permission lists r1, r2 in order to display them in the end
    will return a single permissions list
    """
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2
        self.d_perm = []
        self.n_perm = []
    
    def comp_them(self):
        # the deleted permissions
        exist = False
        diff = {}
        for o1 in self.r1:
            for o2 in self.r2:
                if (str(o1["1"]) == str(o2["1"])):
                    exist = True
                    for e1 in o1:
                        if e1 not in o2:
                            diff[e1] = o1[e1]
                            diff["1"] = o1["1"]
                    self.d_perm.append(diff)
                    diff = {}
            if not exist:
                self.d_perm.append(o1)
            exist = False

        # the added permissions
        exist = False
        diff = {}
        for o2 in self.r2:
            for o1 in self.r1:
                if (str(o1["1"]) == str(o2["1"])):
                    exist = True
                    for e2 in o2:
                        if e2 not in o1:
                            diff[e2] = o2[e2]
                            diff["1"] = o2["1"]
                    self.n_perm.append(diff)
                    diff = {}
            if not exist:
                self.n_perm.append(o1)
            exist = False



# Main
def main():
    parser = argparse.ArgumentParser(prog='data_shark.py',
                                    description='''Pug, allows you to search for a reverse path from a pawnd user
                                    to a suspected attacker. as well as to see the changes between 2 "snapshoots"
                                    of the domain.
                                    ''')
    
    parser.add_argument('-o','--Pug_option', help='choose r for reverse search and c for compare', required=False)
    parser.add_argument('-d','--display', help='shows a single object domain tree', required=False)
    parser.add_argument('-sp','--shortest_path', help='shortest path between 2 users - "source,destination"', required=False)
    parser.add_argument('-da1','--date1', help='first date to compare - "dd-MM-yyyy"', required=False)
    parser.add_argument('-da2','--date2', help='secound date to compare to - "dd-MM-yyyy"', required=False)

    args = vars(parser.parse_args())

    # if the option is to check the dijkstra path
    if args["Pug_option"] == 'r':
        r = reader()
        p = r.permissions
        ok = False
        # checks if the display was acted upon
        if args["display"]:
            od = object_display(p, str(args["display"].lower().replace(" ","")))
            p = od.endGoal
            # maps the permissions
            m = mapper(p)
            m.display()
            ok = True
        if args["shortest_path"]:
            l = args["shortest_path"].lower().replace(" ","").split(",")
            od = object_display(p, l[1])
            p = od.endGoal
            m = mapper(p)
            m.dijkstra_display(l[0],l[1])
            ok = True
        if not ok:
            m = mapper(p)
            m.display()
    
    # run the compare operation
    elif(args["Pug_option"] == "c"):
        # fill date1 and date2 for compare
        if not args["date1"] == "":
            if args["date2"] == "":
                date2 = date.today().strftime("%d/%m/%Y")
            else:
                date2 = args["date2"]
            date1 = args["date1"]
        else:
            print("please specifiy the first date, secound is today by defualt")
        # compare the 2 dates
        r1 = reader(date1).permissions
        r2 = reader(date2).permissions
        c = compare(r1,r2)
        c.comp_them()
        print("new permissions")
        m = mapper(c.n_perm)
        m.display()
        print("deleted permissions")
        m = mapper(c.n_perm)
        m.display()        



    # if no valid option was specified
    else:
        print("not a valid option please choose either 'r' or 'c' see more in help (-h)")
if __name__ == "__main__":
    main()