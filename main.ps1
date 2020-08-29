# IMPORTS
ipmo ac* # import the active directory module

# CONSTS
$Date = get-date -Format dd-MM-yyyy
$users_path = "c:\pug\" + $Date

# Functions
function get-userlist(){
    $users =  Get-ADUser -Filter *
    $users += Get-ADGroup -Filter *
    foreach($user in $users){
        cd $users_path
        $objSID = New-Object System.Security.Principal.SecurityIdentifier `
        ($user.SID.value)
        $objUser = $objSID.Translate( [System.Security.Principal.NTAccount]) -replace "[\\]", "-"
        
        New-Item -ItemType directory -Path $objUser
        cd $objUser
        $f_name = ".\"+ $objUser + ".csv"
        $user | Export-Csv -path $f_name
        $name = "AD:" + $user.DistinguishedName
        $f_name = ".\"+ $user.DistinguishedName + ".txt"
        echo (Get-Acl $name).access > $f_name

        cd $users_path
        
    }
}

function get-itstarting(){
<#
 gets everything started and ready for the usage of pug
#>
    if(! (Test-Path $users_path)){
        New-Item -ItemType directory -Path $users_path
    }
}


# MAIN
function main(){
    get-itstarting
    get-userlist



}
main