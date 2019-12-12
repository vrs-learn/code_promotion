from migration.apiservice import CDP_api
from env.authorize import verify_user, form_url
from env.logging import *

def trigger_migration(sourcecdp_fromdb,sourcerepo_fromdb,destinationcdp_fromdb,user_modules,download_dir,activate):
    log_this = Log_Process()
    list_of_downloaded_mod=[]
    list_of_uploaded_mod=[]
    mod_success=[]
    sourcetso_url=form_url(sourcecdp_fromdb)
    destinationtso_url=form_url(destinationcdp_fromdb)
    sourcetso_repourl=form_url(sourcerepo_fromdb)
    sourcetso = CDP_api(sourcetso_url,sourcecdp_fromdb['username'],sourcecdp_fromdb['password'])
    destinationtso = CDP_api(destinationtso_url,destinationcdp_fromdb['username'],destinationcdp_fromdb['password'])
    sourcetso.login()
    destinationtso.login()
    print("Downloading Modules : \n")
    log_this.logger.info("Downloading Modules")
    for mod in user_modules:
        download_status = sourcetso.download_module(mod['name'],mod['ver'],mod['rev'],sourcetso_repourl,sourcerepo_fromdb['username'],sourcerepo_fromdb['password'],download_dir)
        if download_status == 200:
            x={}
            mod_success.append(mod['name']+"."+mod['ver']+".roar")
            x['name']=mod['name']
            x['ver']=mod['ver']
            list_of_downloaded_mod.append(x)
            print(x)
            log_this.logger.info(mod_success)
        else:
            log_this.logger.error("Download failed for "+ str(mod['name']) + " with status " + str(download_status))
    if len(mod_success) > 0:
        print("List of all downloaded Modules are :\n" + str(mod_success))
        log_this.logger.info("List of all downloaded Modules are" + str(mod_success))
        print("Uploading Modules : \n")
        log_this.logger.info("Uploading Modules")
        for mod in list_of_downloaded_mod:
            mod_name=mod['name']+"."+mod['ver']+".roar"
            destinationtso.upload_module(mod_name,mod_name,download_dir,destinationcdp_fromdb['username'],"Uploading Module","Code Migration")
            if destinationtso.upload_status == 200:
                list_of_uploaded_mod.append(mod)
        if len(list_of_uploaded_mod) > 0 and activate :
            destinationtso.get_all_modules()
            repo_mods=destinationtso.mods_datastore
            get_rev=lambda mod_name,mod_ver,mods_list: [x['revision'] for x in mods_list if x['name']==mod_name and x['version']==mod_ver]
            for mod in list_of_uploaded_mod :
                mod.update({'revision' : get_rev(mod['name'],mod['ver'],repo_mods)[0]})
            destinationtso.activate_module(list_of_uploaded_mod)
        elif len(list_of_uploaded_mod) > 0:
            print("Exiting without activating the Modules.")
            log_this.logger.info("Exiting without activating the Modules")
        else :
            print("Unable to Upload Modules. Check Logs.")
            log_this.logger.info("Unable to Upload Modules. Check Logs")
    sourcetso.logout()
    destinationtso.logout()

def print_env_details(sourcecdp_fromdb,sourcerepo_fromdb,destinationcdp_fromdb):
    log_this = Log_Process()
    print("\nThe current environment details are : \n")
    log_this.logger.info("The current environment details are :")
    print("\t Source CDP :\t\t" + ( "http" if sourcecdp_fromdb['sec_value'] == 0 else "https" ) + "://" + sourcecdp_fromdb['server'] + ":" + str(sourcecdp_fromdb['port']) )
    log_this.logger.info("Source CDP : "+( "http" if sourcecdp_fromdb['sec_value'] == 0 else "https" ) + "://" + sourcecdp_fromdb['server'] + ":" + str(sourcecdp_fromdb['port']))
    print("\t Source REPO :\t\t" + ( "http" if sourcerepo_fromdb['sec_value'] == 0 else "https" ) + "://" + sourcerepo_fromdb['server'] + ":" + str(sourcerepo_fromdb['port']) )
    log_this.logger.info("Source REPO :" + ( "http" if sourcerepo_fromdb['sec_value'] == 0 else "https" ) + "://" + sourcerepo_fromdb['server'] + ":" + str(sourcerepo_fromdb['port']))
    print("\t Destination CDP :\t" + ( "http" if destinationcdp_fromdb['sec_value'] == 0 else "https" ) + "://" + destinationcdp_fromdb['server'] + ":" + str(destinationcdp_fromdb['port']) +"\n" )
    log_this.logger.info("Destination CDP :" + ( "http" if destinationcdp_fromdb['sec_value'] == 0 else "https" ) + "://" + destinationcdp_fromdb['server'] + ":" + str(destinationcdp_fromdb['port']) )
    print("\n")
