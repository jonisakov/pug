# pug

## Goal:
Pug is a CLI tool giving you the user the ability to trace Microsoft domain privileges.
From mapping the privileges on a specific user to mapping the difference between two "snapshots" (in different time spans) Pug will help you the IR or blue team to better focus your effort and to easily find backdoors.

## perquisites:
please install the following library’s for python 3.8:
1) pip install networkx
2) pip install matplotlib
3) pip install argparse
4) pip install re
5) pip install datetime
6) pip install glob
7) pip install os
8) pip install string

please install the following for the PowerShell script:
1) Install-WindowsFeature RSAT-AD-PowerShell (install the active directory module for Powershell)

## how to use:
1) run the powershell script as admin (best to do as a schedualed task on the server)
2) open CMD
3) use python to run the python script with the usage displayed bellow

## usage:
pug-mian.py -o r -- will display the entire domain tree

pug-mian.py -o r -d "user name"  -- will display the domain tree for a specific AD object

pug-mian.py -o r -sp "source object, destination object" -- will display the shortest path (if exists) between the source to destination.

pug -o c -da1 "dd-MM-yyyy" -da2 "dd-MM-yyyy" -- will display the changes between the dates firstly deleted connections then added connections



