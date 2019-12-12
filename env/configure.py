from db.database import Database
from env.authorize import verify_user, form_url
import getpass, sys, os, configparser
from env.logging import *

def get_env_details(db):
    s_cdp = get_env_from_user("CDP","source",1)
    s_repo = get_env_from_user("REPO","source")
    d_cdp = get_env_from_user("CDP","destination",1)
    insert_env_details_to_db(db,s_cdp,s_repo,d_cdp)

def call_validity_check(envdetails,counter):
    url=form_url(envdetails)
    if verify_user(envdetails,envdetails['username'],envdetails['password']):
        return ( envdetails , True )
    elif counter == 1:
        print("Credentials are not valid. Please enter valid creds.")
        return get_env_from_user(envdetails['component'],envdetails['s_or_d'],1,counter)
    else:
        return ( envdetails , False )

def get_env_from_user(component,s_or_d,verify=0,counter=0):
    log_this = Log_Process()
    print("Please enter "+s_or_d+" "+component+" Details :")
    log_this.logger.info("Please enter "+s_or_d+" "+component+" Details ")
    envdetails = {}
    envdetails['server'] = input("Server :\t")
    envdetails['port'] = input("Port :\t")
    sec = input("Secure ( Y or N ) :\t")
    envdetails['sec_value'] = 1 if sec == "Y" else 0
    envdetails['username'] = input("Username :\t")
    envdetails['password'] = getpass.getpass("Password :\t")
    envdetails['component'] = component
    envdetails['s_or_d'] = s_or_d
    if verify == 1:
        envdetails , check = call_validity_check(envdetails,counter+1)
        if check and counter == 0 :
            return envdetails
        elif check and counter == 1:
            return (envdetails, True)
        else :
            print("Credentials are not valid. Exiting the automation")
            log_this.logger.error("Credentials are not valid. Exiting the automation")
            sys.exit(1)
    else :
        return envdetails


def insert_env_details_to_db(database,s_cdp,s_repo,d_cdp): #Enter Source CDP details in Database : (self,server,port,sec_value,username,password,component,s_or_d)
    database.insert(s_cdp['server'],s_cdp['port'],s_cdp['sec_value'],s_cdp['username'],s_cdp['password'],s_cdp['component'],s_cdp['s_or_d'])
    database.insert(s_repo['server'],s_repo['port'],s_repo['sec_value'],s_repo['username'],s_repo['password'],s_repo['component'],s_repo['s_or_d'])
    database.insert(d_cdp['server'],d_cdp['port'],d_cdp['sec_value'],d_cdp['username'],d_cdp['password'],d_cdp['component'],d_cdp['s_or_d'])

def verify_prereq(dir_list):
    for d in dir_list:
        if os.path.isdir(d):
            continue
        else:
            try :
                os.mkdir(d)
            except :
                print("Failed to create "+d+" directory.")
                sys.exit(3)

def display_env(config_filepath):
    log_this = Log_Process(config_filepath)
    config = configparser.ConfigParser()
    config.read(config_filepath)
    db_path=config['ENV']['DB_PATH']
    db = Database(db_path)
    try:
        sourcecdp_fromdb = db.view("CDP","source")
        sourcerepo_fromdb = db.view("REPO","source")
        destinationcdp_fromdb = db.view("CDP","destination")
        if ( len(sourcecdp_fromdb) == 0 ) or ( len(destinationcdp_fromdb) == 0 ) or ( len(sourcerepo_fromdb) == 0 ) :
            print("\nEnvironment Details are inconsistent/unavailable.\n")
        else :
            print("\nThe current environment details are:\n")
            print("\t Source CDP \t\t: " + ( "http" if sourcecdp_fromdb['sec_value'] == 0 else "https" ) + "://" + sourcecdp_fromdb['server'] + ":" + str(sourcecdp_fromdb['port']) )
            print("\t Source REPO \t\t: " + ( "http" if sourcerepo_fromdb['sec_value'] == 0 else "https" ) + "://" + sourcerepo_fromdb['server'] + ":" + str(sourcerepo_fromdb['port']) )
            print("\t Destination CDP \t: " + ( "http" if destinationcdp_fromdb['sec_value'] == 0 else "https" ) + "://" + destinationcdp_fromdb['server'] + ":" + str(destinationcdp_fromdb['port']) +"\n" )
    except KeyboardInterrupt:
        print("Cancelling action as per User Interruption.")
        pass

def clear_env(config_filepath):
    config = configparser.ConfigParser()
    config.read(config_filepath)
    db_path=config['ENV']['DB_PATH']
    database = Database(db_path)
    log_this = Log_Process(config_filepath)
    try :
        log_this.logger.info("Environment Deletion triggered by "+ getpass.getuser())
        user_input=input("Do you want to clear all the environment details ? Enter Y or N :")
        log_this.logger.info("Do you want to clear all the environment details ? Enter Y or N "+ str(user_input))
        if user_input =="Y":
            print("Deleting entire data from "+tsodb)
            log_this.logger.info("Deleting entire data from "+tsodb)
            database.delete_all()
    except KeyboardInterrupt:
        print("Cancelling action as per User Interruption.")
        log_this.logger.exception("Cancelling action as per User Interruption")
        pass

def main(config_filepath):
    config = configparser.ConfigParser()
    config.read(config_filepath)
    db_path=config['ENV']['DB_PATH']
    db = Database(db_path)
    log_this = Log_Process(config_filepath)
    try :
        log_this.logger.info("Environment Configuration triggered by "+ getpass.getuser())
        user_input = input("All previous environment details will be overwritten. \n Do you want to configure the Code Migration env.?  Enter Y or N :")
        log_this.logger.info("All previous environment details will be overwritten. \n Do you want to configure the Code Migration env.?  Enter Y or N :" + str(user_input))
        if user_input == "Y" :
            db.delete_all()
            get_env_details(db)
    except KeyboardInterrupt:
        print("Cancelling the Environment Configuration Setup as per User Interruption.")
        log_this.logger.info("Cancelling the Environment Configuration Setup as per User Interruption")
        pass

####################################################
######################  MAIN #######################
####################################################

tsodb = "tsoenv.db" #Default Database used for storing TSO Environment details.

if __name__=="__main__":
    main()
