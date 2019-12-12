import argparse, interactive, non_interactive, env.configure
from env.env_config import *

####################################################
######################  MAIN #######################
####################################################

config_filepath = set_config_vars(__file__)

parser = argparse.ArgumentParser(description='TSO Code Migration Utility')
group = parser.add_mutually_exclusive_group()
group.add_argument("-i" , "--interactive" ,dest="Interactive", action="store_true", help="For Interactive code migration.")
group.add_argument("-f" , "--file" , dest="Filename", type=argparse.FileType('r'), help="To read modules for code migration from a file. In the file mention -m MODULE_NAME -v VERSION [-r REVISION ]")
group.add_argument("-c" , "--configure" , dest="Configure", action="store_true", help="To configure the tso environment for code migration")
group.add_argument("-d" , "--displayenv", dest="DisplayEnv", action="store_true", help='To Display the current Env Config')
group.add_argument("-deleteEnv" , dest="DeleteEnv", action="store_true", help='To Delete the current Env Config')
parser.add_argument("-a", "--activate", dest="Activate", required=False , action="store_true", help='To activate the Modules. Works only wih -f|--file flag')
parser.add_argument("-m", "--module", dest="Module", required=False, help="Module Name to be pushed. Works only in conjunction with -v/--version")
parser.add_argument("-v", "--version", dest="Version", required=False, help="Version name of the module to be pushed. Works only in conjuction with -m/--module")
parser.add_argument("-r", "--revision", dest="Revision", required=False, help="[Optional] Revision of the Module version. Works only in conjuction with -m/--module & -v/--version")
args = parser.parse_args()

if args.Interactive :
    interactive.main(config_filepath)
elif args.Filename :
    non_interactive.main(args.Filename,args.Activate,config_filepath)
elif args.Configure:
    env.configure.main(config_filepath)
elif args.DisplayEnv:
    env.configure.display_env(config_filepath)
elif args.DeleteEnv:
    env.configure.clear_env(config_filepath)
elif args.Module and args.Version : 
	non_interactive.single_mod(args.Module,args.Version,args.Revision,args.Activate,config_filepath)
else :
    parser.print_help()
