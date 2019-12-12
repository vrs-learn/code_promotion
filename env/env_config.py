import platform, os, sys
import configparser

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

def set_config_vars(filepath):
    config = configparser.ConfigParser()
    if platform.system() == "Windows":
        SCR_PATH, FILE_NAME = os.path.split(os.path.abspath(filepath))
        CONF_FILE=SCR_PATH+"\\config.ini"
        if os.path.isfile(CONF_FILE):
            config.read(CONF_FILE)
            if len(config['ENV']) != 3:
                config['ENV'] = {}
                config['ENV']['LOG_DIR'] = SCR_PATH+"\\logs"
                config['ENV']['DOWNLOAD_DIR'] = SCR_PATH+"\\downloads"
                config['ENV']['DB_PATH'] = SCR_PATH+"\\tsoenv.db"
                with open(CONF_FILE, 'w') as configfile:
                    config.write(configfile)
                LOG_DIR=config['ENV']['LOG_DIR']
                DOWNLOAD_DIR=config['ENV']['DOWNLOAD_DIR']
                verify_prereq([LOG_DIR,DOWNLOAD_DIR])
        else :
            config['ENV'] = {}
            config['ENV']['LOG_DIR'] = SCR_PATH+"\\logs"
            config['ENV']['DOWNLOAD_DIR'] = SCR_PATH+"\\downloads"
            config['ENV']['DB_PATH'] = SCR_PATH+"\\tsoenv.db"
            with open(CONF_FILE, 'w') as configfile:
                config.write(configfile)
            LOG_DIR=config['ENV']['LOG_DIR']
            DOWNLOAD_DIR=config['ENV']['DOWNLOAD_DIR']
            verify_prereq([LOG_DIR,DOWNLOAD_DIR])
        return CONF_FILE
    else :
        if getattr(sys, 'frozen', False):
            SCR_PATH = os.path.dirname(sys.executable)
            FILE_NAME = filepath
        else :
            SCR_PATH, FILE_NAME = os.path.split(os.path.abspath(filepath))
        CONF_FILE=SCR_PATH+"/config.ini"
        if os.path.isfile(CONF_FILE):
            config.read(CONF_FILE)
            if len(config['ENV']) != 3:
                config['ENV'] = {}
                config['ENV']['LOG_DIR'] = SCR_PATH+"/logs"
                config['ENV']['DOWNLOAD_DIR'] = SCR_PATH+"/downloads"
                config['ENV']['DB_PATH'] = SCR_PATH+"/tsoenv.db"
                with open(CONF_FILE, 'w') as configfile:
                    config.write(configfile)
                LOG_DIR=config['ENV']['LOG_DIR']
                DOWNLOAD_DIR=config['ENV']['DOWNLOAD_DIR']
                verify_prereq([LOG_DIR,DOWNLOAD_DIR])
        else :
            config['ENV'] = {}
            config['ENV']['LOG_DIR'] = SCR_PATH+"/logs"
            config['ENV']['DOWNLOAD_DIR'] = SCR_PATH+"/downloads"
            config['ENV']['DB_PATH'] = SCR_PATH+"/tsoenv.db"
            with open(CONF_FILE, 'w') as configfile:
                config.write(configfile)
            LOG_DIR=config['ENV']['LOG_DIR']
            DOWNLOAD_DIR=config['ENV']['DOWNLOAD_DIR']
            verify_prereq([LOG_DIR,DOWNLOAD_DIR])
        return CONF_FILE
