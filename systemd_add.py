import os
import subprocess
import venv

version = '1.0'
accept_value = ['y', 'yes', '1', 1]
none_value = ['none', 'no', 'n', '', None]
maindir = os.getcwd()
linux_pkgmgr = 'apt'



#option1
def create_service1(sdn, wdir, usr, hprot, sdesc):
    print(f'Creating {sdn}.service in /etc/systemd/system..')
    try:
        with open(f'/etc/systemd/system/{sdn}.service', 'w') as sys:
            sys.write(f"""[Unit]
Description={sdesc}\n
[Service]
ExecStart={wdir}/SSCK/autorun.sh
User={usr}
WorkingDirectory={wdir}
ProtectHome={hprot}\n
[Install]
WantedBy=multi-user.target
""")
        print("Done!")
        print(f"Run post installation commands to enable {sdn}.service to start with system startup:\nsudo chmod 775 -R {wdir}/* -> If it's not executable\nsudo systemctl enable {sdn} -> Enables automatic startup\nsudo systemctl start  {sdn} -> Optional (turns on service)\nsudo systemctl daemon-reload -> to reload the daemon\nREMEMBER about Reading/Executing permissions for others If something will not work!")
    except Exception as err:
        print(f'Error occurred: {err}')
        exit()

    #o1-def
def cs1_default(wdir, filename):
    print("Making autorun.sh file..")
    try:
        if os.path.exists(f'{wdir}/SSCK') == False:
            os.makedirs(f'{wdir}/SSCK')
            os.chmod(f'{wdir}/SSCK', 0o775)
        with open(f'{wdir}/SSCK/autorun.sh', 'w') as auto:
            auto.write(f"#!/bin/bash\ncd {wdir}\npython3 {filename}")
        os.chmod(f'{wdir}/SSCK/autorun.sh', 0o775)
        print('Done.')
    except Exception as err:
        print(f"Can't create file!\nException: {err}")
        exit()

    #o1-venv
def cs1_venv(wdir, filename, venv):
    print('Making autorun.sh file..')
    try:
        if os.path.exists(f'{wdir}/SSCK') == False:
            os.makedirs(f'{wdir}/SSCK')
            os.chmod(f'{wdir}/SSCK', 0o775)
        with open(f'{wdir}/SSCK/autorun.sh', 'w') as auto:
            auto.write(f'#!/bin/bash\ncd {wdir}\n{wdir}/{venv}/bin/python3 {filename}')
        os.chmod(f'{wdir}/SSCK/autorun.sh', 0o775)
        print('Done.')
    except Exception as err:
        print(f"Can't create file!\nException: {err}")
        exit()


#option4
def create_command(cmd, sdn, wdir, usr, hprot, sdesc):
    print(f'Creating {sdn}.service in /etc/systemd/system..')
    try:
        with open(f'/etc/systemd/system/{sdn}.service', 'w') as sys:
            sys.write(f"""[Unit]
Description={sdesc}\n
[Service]
ExecStart={cmd}
User={usr}
WorkingDirectory={wdir}
ProtectHome={hprot}\n
[Install]
WantedBy=multi-user.target
""")
        print("Done!")
        print(f"Run post installation commands to enable {sdn}.service to start with system startup:\nsudo chmod 775 -R {wdir}/* -> If it's not executable\nsudo systemctl enable {sdn} -> Enables automatic startup\nsudo systemctl start {sdn} -> Optional (turns on service)\nsudo systemctl daemon-reload -> to reload the daemon\nREMEMBER about Reading/Executing permissions for others If something will not work!")


    except Exception as err:
        print(f'Error occurred: {err}')
        exit()



#   Select working directory
def workdir():
    ask = input(f"Should '{maindir}' be a working directory? [y/N]: ")
    if ask.lower() in accept_value:
        return maindir
    else:
        return input("Type the full path of your working directory: ")


#   Check if you're using python3 venv
def is_venv():
    is_venv_name=None
    ask = input("Do you use python3 venv? You can now Create one if you need [y/N/C]: ")
    if ask.lower() in ['c', 'create']:
        is_venv_name = input("Enter directory name for virtual environment: ")
        try:
            print("Installing python3-venv...")
            subprocess.run(['sudo', linux_pkgmgr, 'update', '-y'], check=True)
            subprocess.run(['sudo', linux_pkgmgr, 'install', 'python3-venv', '-y'], check=True)
            venv.create(is_venv_name, with_pip=True)
        except Exception as err:
            print(f"Failed to create venv: {err}")
            is_venv_name=None

    if ask.lower() in accept_value or ask.lower() in ['c', 'create']:
        if is_venv_name:
            print(f"[python3 venv]: {is_venv_name}")
            return is_venv_name
        else:
            return input('Enter python3 venv directory name: ')
    else:
        print("[python3 venv]: False")
        return 'None'


#   Who should run this service - root for default
def sel_user():
    ask = input("Select user running the service (None for root as default): ")
    if ask.lower() in none_value:
        return 'root'
    else:
        return ask
    

#   Home Directory Protection
def prot_home():
    ask = input("Do you want to disable home directory protection (not recommended)? [y/N]: ")
    if ask.lower() in accept_value:
        return 'no'     # Yes, I want to disable HDP so we put no to disable it in systemd file
    else:
        return 'yes'    # No, I don't want to disable HDP so we put yes to enable it in systemd file


#   Description for systemd service
def description(name):
    ask = input("Type description for your service (None for default): ")
    if ask.lower() in none_value:
        return f"{name} autorun service"
    else:
        return ask


#   Path to python
def python_path(work_dir, venv_name):
    path = 'None'
    if venv_name != 'None':
        path = f"{work_dir}/{venv_name}/bin/python3"
        if os.path.exists(path):
            print(f"[python_path] Detected {path}")
        else:
            print(f"[python_path] Can't detect python3 in venv path: {path}")
            path = 'None'
    
    print(f"""Select python3 path:
1 - /usr/bin/python3
2 - python3 from virtual environment ({path})
3 - other""")
    ask = int(input(">>> "))
    if ask == 1:
        return '/usr/bin/python3'
    elif ask == 2:
        return path if path != 'None' else input("Enter custom python3 path: ")
    elif ask == 3:
        return input("Enter custom python3 path: ")




#   The Beginning
print(f"""SYSTEMD SERVICE CREATOR  v{version}
##################################

This tool will add your script to system startup (autostart) using systemd.
You should run this tool as root in your main directory.
""")
print(f'Detected current dir: {maindir}')
print(f"""If this directory:
- Is your main (root) directory of your script you want to add to systemd
- Includes python3 virtual environment directory (If you need it for python script; you can make venv later)
- Can be changed by chmod to 775 permissions

We can start. If not, You should change it to proper directory.\nThere's option later to change working directory if you want to.\n""")

check = input("Do you want to start? [y/N]: ")

if check.lower() in accept_value:

    print(f"""Select method of how do you want to run your script:
1 - Run python file using .sh file (.py)
2 - Run shell script (.sh)
3 - Run python file (.py)
4 - Run specific bash/shell command
""")
    try:
        type_check = int(input(">>> "))
    except:
        print("Invalid input. Aborting...")
        exit()

    print(f"Selected Main Directory: {maindir}")

    file_name = 'None'
    systemd_name = 'None'
    work_dir = 'None'
    venv_name = 'None'
    user = 'root'
    home_prot = 'yes'
    serv_description = 'None'
    py_path = 'None'
    command = 'None'
    venv_loc = 'None'

    if type_check == 1:
        file_name = input("Enter your python file name (without '.py' extension): ")+".py"
        systemd_name = input("Enter name for your systemd service (without '.service'): ")
        work_dir = workdir()
        venv_name = is_venv()
        user = sel_user()
        home_prot = prot_home()
        serv_description = description(systemd_name)

    
    elif type_check == 2:
        file_name = input("Enter your shell script name (without '.sh' extension): ")+".py"
        systemd_name = input("Enter name for your systemd service (without '.service'): ")
        work_dir = workdir()
        user = sel_user()
        home_prot = prot_home()
        serv_description = description(systemd_name)


    elif type_check == 3:
        file_name = input("Enter your python file name (without '.py' extension): ")+".py"
        systemd_name = input("Enter name for your systemd service (without '.service'): ")
        work_dir = workdir()
        venv_name = is_venv()
        user = sel_user()
        home_prot = prot_home()
        serv_description = description(systemd_name)
        py_path = python_path(work_dir, venv_name)


    elif type_check == 4:
        command = input('Type your command which you want to execute: ')
        systemd_name = input("Enter name for your systemd service (without '.service'): ")
        work_dir = workdir()
        user = sel_user()
        home_prot = prot_home()
        serv_description = description(systemd_name)


    else:
        print('Wrong method selected!')
        exit()



    systemd_name_path = f"/etc/systemd/system/{systemd_name}.service"

#   Summary
    print('\nOK.')
    print("SSCK will create files by following informations:\n")
    print(f"File name:                                      {file_name}") if file_name not in none_value else print("File name:                                      Not set")
    print(f"Service name:                                   {systemd_name}")
    print(f"Service description:                            {serv_description}")
    print(f"Systemd entry location:                         {systemd_name_path}")
    print(f"Working directory:                              {work_dir}") if work_dir not in none_value else print("Working directory:                      Not set")
    print(f"Run by user:                                    {user}")
    print(f"Home directory protection:                      {home_prot}")

    if type_check == 1:
        auto_sh_path = f"{work_dir}/SSCK/autorun.sh"
        print(f"autorun.sh location:                            {auto_sh_path}")

    if (type_check == 1 or type_check == 3) and venv_name not in none_value:
        print(f"Python3 virtual environment (venv) name:        {venv_name}")
        venv_loc = f"{work_dir}/{venv_name}"
        print(f"Venv location:                                  {venv_loc}")

    if type_check == 3:
        print(f"Python3 path:                                   {py_path}")

    if type_check == 4:
        print(f"Command to execute:                             {command}")

    print("#" * 20)
#   Veryfying paths
    print("\nVerifying path existence..")

    try:
        if os.path.exists(work_dir):
            print(f"{work_dir} path OK.")
        else:
            print(f"{work_dir} not found!") if work_dir not in none_value else print("Working directory not set, skipping path check.")

        if type_check in (1,2,3):
            if os.path.exists(f'{work_dir}/{file_name}'):
                print(f"{work_dir}/{file_name} path OK.")
            else:
                print(f"{work_dir}/{file_name} not found!") if (work_dir not in none_value or file_name not in none_value) else print("Working directory or file name not set, skipping path check.")

        if os.path.exists('/etc/systemd/system/'):
            print("/etc/systemd/system/ path OK.")
        else:
            print("/etc/systemd/system/ not found!")

        if (type_check == 1 or type_check == 3) and venv_name not in none_value:
            if os.path.exists(venv_loc):
                print(f"{venv_loc} path OK.")
            else:
                print(f"{venv_loc} not found!")

        if type_check == 3:
            if os.path.exists(py_path):
                print(f"{py_path} path OK.")
            else:
                print(f"{py_path} not found!")

    except Exception as err:
        print(f"Failed to verify paths!\nPossible cause: {err}")


    check2 = input("Are you ready to start? [y/N]: ")
    if check2.lower() in accept_value:
        try:
            if type_check == 1:
                if venv_name in none_value:
                    cs1_default(work_dir, file_name)
                else:
                    cs1_venv(work_dir, file_name, venv_name)
                create_service1(systemd_name, work_dir, user, home_prot, serv_description)

            elif type_check == 2:
                print('placeholder')

            elif type_check == 3:
                print('placeholder')

            elif type_check == 4:
                create_command(command, systemd_name, work_dir, user, home_prot, serv_description)

        except Exception as err:
            print(f"Error occurred while creating systemd service entry\nPossible cause: {err}")
    else:
        print('Aborting...')
        exit()
else:
    print('User canceled. Aborting...')
    exit()
