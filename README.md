# README

# TSO Code Migration Utility
TSO Code Migration Utility is used for migrating contents from one environment to another. This utility stores the source and destination environment details in a sqlite db file. The credentials are stored in an encrypted format. Below is a brief of how to use Code migraiton utility. 
Source environment is used to designate the environment from where the modules will be picked up.
Destination environment is used to designate the environment where the modules will be pushed to.

## Getting Started

### Prerequisites
Although the utility is written in python, its compiled into a single executable. The utility is compiled with all its dependent packages into a single file. Therefore there are no prerequisite steps.

### Installing
The code migration utility installer differs for Windows and Linux platform. 

#### Installation for Windows :
```
* Run the setup.exe file
* Select the directory where the utility will be stored
* Installation completed
```

#### Installation for Linux :
```
* Execute the setup.sh file ( Make sure the file has execute permissions )
* Select the directory where the utility will be stored
* Installation completed
```

## Help

To know details of the utility, it can be run as 
```
code_migration -h 
OR
code_migration --help
```

## Configure Code Migration Environment

Before using the Code Migration utility, environment needs to be configured.
execute code_migration via a command prompt ( in Windows ) or in a shell ( in Linux )
```
code_migration -c
OR
code_migration --configure
```
After running, the utility will prompt for Source and Destination environments
To configure the code migration you need details of :
```
Provide following details of Source CDP, Source REPO and Destination CDP 
* Hostname
* Port
* Secure Connection ( for http/https )
* Username
* Password
```

## Displaying Code Migration Environment

To display the Source and Destination environment details, run the utility as below :
```
code_migration -d
OR
code_migration --displayenv
```

## Running the Code migration utility 
Code migration utility allows to trigger the utility in two ways

### Interactive Mode 
To execute the utility in interactive mode, run as below 
```
code_migration -i
OR
code_migration --interactive
```

#### Activating Modules in Interactive Mode
After entering the modules, versions and revisions, the option for activating the modules is prompted.
You can enter Y at the prompt if you want the modules to be activated.

### Non-Interactive Mode 
To execute the utility in non-interactive mode, a file is required as input param.
```
code_migration -f <FILENAME>
OR
code_migration --file <FILENAME>
```
The contents in the file should be as below 
```
* -m MODULE_NAME -v VERSION ( This downloads the module with the version and latest revision )
* -m MODULE_NAME -v VERSION -r REVISION ( This downloads the module with the version and specific revision mentioned )
```
#### Activating Modules in Non-Interactive Mode
If you want the modules to be activated after being migrated to the destination environment, you can enter "-a" flag
```
code_migration -f <FILENAME> -a
OR
code_migration --file <FILENAME> -a
```

## Logging 
Execution of the code migration utility creates logs which can be further used to identify if there are any failures.
The utility creates a log for each execution with the timestamp in the logs directory.

## Deleting the Environment Details
If you wish to remove all the environment details stored, you can use the -deleteEnv flag. 
This will delete all the environment details
```
code_migration -deleteEnv
```
