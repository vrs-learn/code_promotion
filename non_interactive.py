from migration.apiservice import CDP_api
from migration.action import *
from db.database import Database
from env.configure import get_env_details , verify_prereq
from env.authorize import verify_user, form_url
from env.logging import *
import getpass , time , argparse, configparser


def get_args(row):
    x={}
    parser=argparse.ArgumentParser(description=' Parsing the Modules from the file.')
    parser.add_argument("-m" , "--module" , dest="ModuleName", help="Module Name to be migrated", required=True)
    parser.add_argument("-v" , "--version" , dest="Version", help="Version of the Module",required=True)
    parser.add_argument("-r" , "--revision" , dest="ReVision", default="", help="Revision of the Version of the Module")
    args = parser.parse_args(row.split())
    x['name']=args.ModuleName
    x['ver']=args.Version
    x['rev']=args.ReVision
    return x

def main(file_content,activate,config_filepath):
    config = configparser.ConfigParser()
    config.read(config_filepath)
    download_dir=config['ENV']['DOWNLOAD_DIR']
    db_path=config['ENV']['DB_PATH']
    log_this = Log_Process(config_filepath)
    log_this.logger.info("Non-Interactive Code Migration initiated by : "+ getpass.getuser())
    try :
        print("\nRunning the Non Interactive Mode of Code Migration utility.")
        log_this.logger.info("Running the Non Interactive Mode of Code Migration utility.")
        user_modules=[]
        for line in file_content:
            mods=get_args(line)
            user_modules.append(mods)
        print("\nUser Modules to be migrated are : ")
        print(user_modules)
        log_this.logger.info("User Modules to be migrated are : " +str(user_modules))
        if len(user_modules) > 0 :
            tsodb = db_path #DB used for storing the environment credentials
            database = Database(tsodb)
            sourcecdp_fromdb = {}
            sourcerepo_fromdb = {}
            destinationcdp_fromdb = {}
            sourcecdp_fromdb = database.view("CDP","source")
            sourcerepo_fromdb = database.view("REPO","source")
            destinationcdp_fromdb = database.view("CDP","destination")
            if ( len(sourcecdp_fromdb) == 0 ) or ( len(destinationcdp_fromdb) == 0 ) or ( len(sourcerepo_fromdb) == 0 ) :
                print("\n The Environment details are inconsistent or do not exist. Please use -c to configure the Source and destination details.")
                log_this.logger.info("The Environment details are inconsistent or do not exist. Please use -c to configure the Source and destination details")
                sys.exit(4)
            else :
                print_env_details(sourcecdp_fromdb,sourcerepo_fromdb,destinationcdp_fromdb)
                trigger_migration(sourcecdp_fromdb,sourcerepo_fromdb,destinationcdp_fromdb,user_modules,download_dir,activate)
        else :
            print("\n Unable to parse the Modules and versions from the file.")
            log_this.logger.warning("Unable to parse the Modules and versions from the file")
    except KeyboardInterrupt as e:
        print("Cancelling the Code Migration as per User Interruption.")
        log_this.logger.exception("Cancelling the Code Migration as per User Interruption.")
        pass
    except :
        print("Code Migration failed. Please check logs.")
        log_this.logger.exception("Code Migration failed. Please check for errors.")
        pass

####################################################
######################  MAIN #######################
####################################################

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='TSO Code Migration Utility - Non-Interactive Mode')
    parser.add_argument("-f" , "--file" , dest="Filename", type=argparse.FileType('r'), help="To read modules for code migration from a file. In the file mention -m MODULE_NAME -v VERSION")
    parser.add_argument("-a", "--activate", dest="Activate", required=False , action="store_true", help='To activate the Modules. Works only with -f|--file flag')
    args = parser.parse_args()
    if args.Filename:
        main(args.Filename,args.Activate)
