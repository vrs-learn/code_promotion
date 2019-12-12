import logging , configparser , time, platform

def logobj(cls):
    instances={}
    def get_instance(config_filepath=None):
        if cls not in instances:
            instances[cls]=cls(config_filepath)
        return instances[cls]
    return get_instance


@logobj
class Log_Process():

    def __init__(self,config_filepath=None):
        config = configparser.ConfigParser()
        config.read(config_filepath)
        log_dir=config['ENV']['LOG_DIR']
        log_time=str(time.localtime().tm_year)+"_"+str(time.localtime().tm_mon)+"_"+str(time.localtime().tm_mday)+"_"+str(time.localtime().tm_hour)+"_"+str(time.localtime().tm_min)+"_"+str(time.localtime().tm_sec)
        self.logger = logging.getLogger("code_migration")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
        #define file handler
        if platform.system() == "Windows" :
            file_handler = logging.FileHandler(log_dir+"\\code_migration_"+log_time+".log")
        else :
            file_handler = logging.FileHandler(log_dir+"/code_migration_"+log_time+".log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        #add file handler
        self.logger.addHandler(file_handler)

    def set_stream(self):
        #define stream handler
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        #add the stream handlers
        self.logger.addHandler(stream_handler)
