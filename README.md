# GDB_DomainCleanup

##Description
Reads in command line arguements for listing and deleting Esri unused geodatabases domains.  For SDE geodatabases, the script must be run as the owner of the domain for the delete option to function
 
## Credits
Thanks to Blake T. for sharing his original script.  This script is an adaptation of the original.   
 
##Command Line Example: 
 
 GDB_DomainCleanup.py -c "C:\Testing\Connections\myGDB.sde" -l "C:\Testing\DuplicateDomain.log" -d
 
 Command Line Arguments:
 * -c: Geodatabase connection - SDE, file or personal geodatabase
 * -l: Log file - Unused domains output to text file
 * -d: Delete flag (optional) - WILL DELETE DOMAIN IF FLAG IS PRESENT!
