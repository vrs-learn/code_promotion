import requests, json, sqlite3, getpass , platform
from env.logging import *

class CDP_api:

    def __init__(self, url, user, passw):
        self.log_this = Log_Process()
        self.url=url
        self.login_url=self.url+"/baocdp/rest/login"
        self.logout_url=self.url+"/baocdp/rest/logout"
        self.header={"username" : user, "password" : passw}
        requests.packages.urllib3.disable_warnings()

    def login(self):
        try :
            self.login_r=requests.post(self.login_url, json=self.header,verify=False)
            self.login_status_code=self.login_r.status_code
            if self.login_status_code == 200:
                self.auth_token=self.login_r.headers['Authentication-Token']
                self.log_this.logger.info("User authenticated successfully for "+str(self.url))
            else :
                self.auth_token=""
                self.log_this.logger.error("User authentication failed or TSO env "+str(self.url)+" failed to reply. Return Code :" + str(self.login_status_code) )
                self.log_this.logger.error(self.login_r.text)
        except :
            print("Connection unavailable.")
            self.log_this.logger.exception("Connection unavailable using "+str(self.url))
            self.login_r=""
            self.login_status_code=""
            self.auth_token=""

    def logout(self):
        try :
            self.logout_header = { "Authentication-Token" : self.auth_token }
            self.logout_r = requests.post(self.logout_url,headers=self.logout_header,verify=False)
            self.log_this.logger.info("Logged out of TSO "+str(self.url)+" successfully")
        except:
            self.log_this.logger.exception("Log out of TSO failed on "+str(self.url))

    def get_all_modules(self):
        try :
            self.get_all_mods_header={ "Authentication-Token" : self.auth_token }
            #self.get_all_processes_url=self.url+"/baocdp/rest/module?pattern=^[a-zA-Z0-9_-]{1,50}"
            self.get_all_mods_url=self.url+"/baocdp/rest/module?repo=true"
            self.mods_req=requests.get(self.get_all_mods_url,headers=self.get_all_mods_header,verify=False)
            self.mods_datastore = json.loads(self.mods_req.text)
            self.log_this.logger.info("Retrieved modules successfully from "+str(self.url))
        except:
            self.log_this.logger.exception("Retrieving Modules failed")

    def download_module(self,module_name,module_ver,module_rev,repo_url,repo_user,repo_pass,download_dir):
        try:
            module=module_name+"."+module_ver+".roar"
            if platform.system() == "Windows" :
                module_loc=download_dir+"\\"+module
            else :
                module_loc=download_dir+"/"+module
            if len(str(module_rev)) > 0:
                self.download_module_url=repo_url+"/baorepo/resources/"+module+";revision="+module_rev
            else : 
                self.download_module_url=repo_url+"/baorepo/resources/"+module
            #print("Module URL which is going to be dowloaded : ", self.download_module_url )
            sess = requests.Session()
            sess.verify=False
            sess.auth=(repo_user,repo_pass)
            module_r = sess.get(self.download_module_url)
            if module_r.status_code == 200:
                print("Module "+module_name+" successfully downloaded.")
                open(module_loc,'wb').write(module_r.content)
                self.log_this.logger.info("Downloaded Module "+str(module)+" successfully")
            else:
                print("Failed to download module "+module_name+" with error code "+str(module_r.status_code))
                self.log_this.logger.error("Failed to download module "+str(module)+" with return code "+ str(module_r.status_code))
                self.log_this.logger.error(module_r.text)
            return module_r.status_code
        except:
            self.log_this.logger.exception("Module download failed with exception for "+str(module_name))
            return 400

    def upload_module(self,module_name,filename,download_dir,author,desc,comments=""):
        try:
            self.upload_url=self.url+"/baocdp/rest/resource/upload"
            self.upload_header={ "Authentication-Token" : self.auth_token, "Resource-Author" : author , "Resource-Description" : desc , "Resource-Comments" : comments}
            if platform.system() == "Windows" :
                file_loc=download_dir+"\\"+filename
            else:
                file_loc=download_dir+"/"+filename
            files={'file' : (filename , open(file_loc, 'rb'))}
            self.upload_req = requests.post(self.upload_url,files=files,headers=self.upload_header,verify=False)
            self.upload_status=self.upload_req.status_code
            if self.upload_status == 200:
                print("Module "+module_name+" successfully uploaded.")
                self.log_this.logger.info("Module "+module_name+" successfully uploaded.")
            else:
                print("Failed to upload module "+module_name+" with error code "+str(self.upload_status))
                print(self.upload_req.text)
                self.log_this.logger.error("Failed to upload module "+module_name+" with error code "+str(self.upload_status))
                self.log_this.logger.error(self.upload_req.text)
        except:
            self.log_this.logger.exception("Failed to Upload Module "+module_name)


    def activate_module(self, module_list):
        try:
            activate_url=self.url+"/baocdp/rest/module/activate"
            activate_header={ "Authentication-Token" : self.auth_token }
            activate_req_body=[]
            for mod in module_list:
                x={}
                x={'name':mod['name'], 'version':mod['ver'], 'revision':mod['revision']}
                activate_req_body.append(x)
            self.log_this.logger.info(activate_req_body)
            self.activate_req=requests.post(activate_url,json={'modules':activate_req_body},headers=activate_header,verify=False)
            if self.activate_req.status_code == 200:
                print("\nModules Activated successfully")
                self.log_this.logger.info("Activate Request status ")
                self.log_this.logger.info(self.activate_req.text)
            else:
                print("Modules Activation failed with return code: "+str(self.activate_req.status_code))
                self.log_this.logger.error("Activation failed ")
                self.log_this.logger.error(self.activate_req.text)
        except:
            self.log_this.logger.exception("Failed to Activate Modules")


#tso = Tso_api("http://clm-aus-018787:38080/baocdp")
#tso.login()
