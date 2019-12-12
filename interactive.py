from migration.apiservice import CDP_api
from migration.action import *
from db.database import Database
from env.configure import get_env_details , verify_prereq
from env.authorize import verify_user, form_url
from env.logging import *
import getpass , time, configparser

def compare_user_and_repo_mods(user,repo):
    repo_mods=[]
    final_mods=[]
    for a in repo:
        repo_mods.append(a['name'])
    if ( len(user) != 0 ) and ( len(repo_mods) != 0 ):
        for user_mod in user:
            if user_mod not in repo_mods:
                print("Module "+user_mod+" does not exists in Repository")

def get_user_inputs():
    log_this = Log_Process()
    print("Enter the Modules you want to download : \n")
    log_this.logger.info("Enter the Modules you want to download")
    mods = []
    check = "Y"
    while check == "Y":
        x={}
        x['name'] = input("Enter the mod name : ")
        x['ver'] = input("Enter the version : ")
        x['rev'] = input("Enter revision [Press enter for latest OR specific number] : ")
        mods.append(x)
        check = input("Do you want to download another module ? Enter Y or N :")
    return mods

def main(config_filepath):
    config = configparser.ConfigParser()
    config.read(config_filepath)
    download_dir=config['ENV']['DOWNLOAD_DIR']
    db_path=config['ENV']['DB_PATH']
    log_this = Log_Process(config_filepath)
    log_this.logger.info("Interactive Code Migration initiated by : "+ getpass.getuser())
    try :
        tsodb = db_path #DB used for storing the environment credentials
        database = Database(tsodb)
        sourcecdp_fromdb = {}
        sourcerepo_fromdb = {}
        destinationcdp_fromdb = {}
        sourcecdp_fromdb = database.view("CDP","source")
        sourcerepo_fromdb = database.view("REPO","source")
        destinationcdp_fromdb = database.view("CDP","destination")
        if ( len(sourcecdp_fromdb) == 0 ) or ( len(destinationcdp_fromdb) == 0 ) or ( len(sourcerepo_fromdb) == 0 ) :
            print("Environment Details are inconsistent/unavailable. Please enter the details.")
            log_this.logger.warning("Environment Details are inconsistent/unavailable. Please enter the details.")
            database.delete_all()
            get_env_details(database)
            sourcecdp_fromdb = database.view("CDP","source")
            sourcerepo_fromdb = database.view("REPO","source")
            destinationcdp_fromdb = database.view("CDP","destination")
            user_modules = get_user_inputs()
            user_activate_check=input("\nDo you want to activate the Modules in Destination ? Enter Y or N : ")
            user_activate_check=True if user_activate_check == "Y" else False
            trigger_migration(sourcecdp_fromdb,sourcerepo_fromdb,destinationcdp_fromdb,user_modules,download_dir,user_activate_check)
        else :
            print_env_details(sourcecdp_fromdb,sourcerepo_fromdb,destinationcdp_fromdb)
            confirm_to_proceed = input("Do you want to continue with the above Env Config ? Enter Y or N :")
            log_this.logger.info("User confirmation to proceed with migration : " + confirm_to_proceed)
            if confirm_to_proceed == "Y":
                print("Enter authorized user for migration :")
                log_this.logger.info("Enter authorized user for migration :")
                exec_user=input("Username : ")
                log_this.logger.info("Code Migration User :" + exec_user )
                exec_pass=getpass.getpass("Password : ")
                if verify_user(sourcecdp_fromdb,exec_user,exec_pass):
                    time.sleep(1)
                    user_modules = get_user_inputs()
                    user_activate_check=input("\nDo you want to activate the Modules in Destination ? Enter Y or N : ")
                    user_activate_check=True if user_activate_check == "Y" else False
                    print(" \n Proceeding with the Migration : \n")
                    log_this.logger.info("Proceeding with the Migration")
                    trigger_migration(sourcecdp_fromdb,sourcerepo_fromdb,destinationcdp_fromdb,user_modules,download_dir,user_activate_check)
                else:
                    print("User Not Authorized to perform action. Exiting")
                    log_this.logger.warning("User Not Authorized to perform action. Exiting")
            else :
                delete_all_confirm=input("Do you want to delete old env and enter new details for Source and Destination env ? Enter Y or N :")
                if delete_all_confirm == "Y":
                    database.delete_all()
                    get_env_details(database)
                    sourcecdp_fromdb = database.view("CDP","source")
                    sourcerepo_fromdb = database.view("REPO","source")
                    destinationcdp_fromdb = database.view("CDP","destination")
                    user_modules = get_user_inputs()
                    user_activate_check=input("\nDo you want to activate the Modules in Destination ? Enter Y or N : ")
                    user_activate_check=True if user_activate_check == "Y" else False
                    trigger_migration(sourcecdp_fromdb,sourcerepo_fromdb,destinationcdp_fromdb,user_modules,download_dir,user_activate_check)
                else:
                    print("Exiting the Migration as No options selected")
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
    parser = argparse.ArgumentParser(description='TSO Code Migration Utility - Interactive Mode')
    parser.add_argument("-i" , "--interactive" ,dest="Interactive", action="store_true", help="For Interactive code migration.")
    args = parser.parse_args()
    main()
