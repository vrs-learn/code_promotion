#
#
from migration.apiservice import CDP_api

def form_url(dict):
    return ("http" if dict['sec_value'] == 0 else "https" ) + "://" + dict['server'] + ":" + str(dict['port'])

def verify_user(cdp_dict,exec_user,exec_pass):
    tso_url=form_url(cdp_dict)
    tso=CDP_api(tso_url,exec_user,exec_pass)
    tso.login()
    if tso.login_status_code == 200:
        return True
    else :
        return False

###########
### MAIN ##
###########

if __name__=="__main__":
    s_url=input("Enter source url :")
    d_url=input("Enter destination url :")
    exec_user=input("Enter User : ")
    exec_pass=input("Enter Pass : ")
    #verify_user(s_url,d_url,exec_user,exec_pass)
