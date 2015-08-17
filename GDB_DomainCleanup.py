import arcpy   
import sys, getopt
import logging
from operator import attrgetter
import os

  
def main(argv):
    print 'start'
    
    try:
        opts, args = getopt.getopt(argv,"c:l:d",["gdbconn=","logfile=","delete"])
    except getopt.GetoptError:
        print 'test.py -c <geodatabaseconnection> -l <logfile> -d'
        sys.exit(2)

    print 'parse options'
    blnDelete = False
    for o, a in opts:
        if o in ("-c", "--gdbconn"):
            myGDB = a
        elif o in ("-d", "--delete"):
            blnDelete = True
        elif o in ("-l", "--logfile"):
            LOG_FILENAME = a
        else:
            assert False, "unhandled option"

    # Set up logging
    #LOG_FILENAME =  r"C:\development\Testing\DuplicateDomain.log"
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename= LOG_FILENAME,
                    filemode='w')
    try:  
        # Connection path to geodatabse (as administrator if SDE)  
        # Get domains that are assigned to a field  
        domainsUsed_names = []  
        for dirpath, dirnames, filenames in arcpy.da.Walk(myGDB, datatype=["FeatureClass", "Table"]):  
            for filename in filenames:  
                print "Checking {}".format(os.path.join(dirpath, filename))  
                ## Check for normal field domains  
                for field in arcpy.ListFields(os.path.join(dirpath, filename)):  
                    if field.domain:  
                        domainsUsed_names.append(field.domain)  
                ## Check for domains used in a subtype field  
                subtypes = arcpy.da.ListSubtypes(os.path.join(dirpath, filename))  
                for stcode, stdict in subtypes.iteritems():  
                    if stdict["SubtypeField"] != u'':  
                        for field, fieldvals in stdict["FieldValues"].iteritems():  
                            if not fieldvals[1] is None:  
                                domainsUsed_names.append(fieldvals[1].name)  
                ## end for subtypes  
            ## end for filenames  
        ## end for geodatabase Walk  
  
        # List of all existing domains (as domain objects)  
        domainsExisting = arcpy.da.ListDomains(myGDB)  
  
        # Find existing domain names that are not in use (using set difference)  
        domainsUnused_names = (  
            set([dom.name for dom in domainsExisting]) - set(domainsUsed_names)  
        )  
  
        # Get domain objects for unused domain names  
        domainsUnused = [  
            dom for dom in domainsExisting  
            if dom.name in domainsUnused_names  
        ]  
        
        #print "{} unused domains in {}".format(len(domainsUnused), myGDB)  
        logging.info( "{} unused domains in {}".format(len(domainsUnused), myGDB))
    except:
        logging.info('Failed generate unused domain list!')
        sys.exit(2)
    finally:  
        # Cleanup  d
        arcpy.ClearWorkspaceCache_management() 
     

        #Print and optionally delete unused domains
        for dom in sorted(domainsUnused, key=attrgetter('owner', 'name')):
            logging.info(dom.owner + " " + dom.name)
            if blnDelete:
                try:
                    arcpy.DeleteDomain_management(myGDB, dom.name)
                    logging.info("Deleted " + dom.owner + " " + dom.name)     
                except:
                    logging.info("Failed to delete " + dom.owner + " " + dom.name)
        arcpy.ClearWorkspaceCache_management()  

if __name__ == '__main__':  
   main(sys.argv[1:])