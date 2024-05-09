import subprocess
import sys

class System:
    """Class to use system commands, similar to that of the os module, but newly implemented"""

    def __init__(self, operating_platform):
        """Initializes the base system and then uses specific commands
        
        Args:
            operating_platform (str):
                The Type of Platform ('Linux', 'Windows').

                If you are not Sure (If you are a noob), use:
                from al import System
                import platform

                system = System(platform.system())
        """
        self.operating_platform = operating_platform

    def run(self, command): # System Command 
        """Executes a command
        
        Args:
            command (str):
                The Command which do you want Execute.
        """
        command = command.split() # Split the Command
        subprocess.run(command) # Execute the Command

    def mkdir(self, *paths): # Create Dir
        """Create The Directorys, but not Sub Directorys
        
        Args:
            *paths (str):
                The Paths which you want Create.
        """
        for path in paths: # Create Slife for all paths
            if self.operating_platform == 'Linux': # Command for Linux Platform
                command = f"mkdir {path}"
            elif self.operating_platform == 'Windows': # Command for Windows Platform
                command = f"mkdir {path}"
            else: # If the Platform not Linux or Windows
                print("Invalid Platform")
                sys.exit(1)
            self.run(command) # Execute the Command

    def makedirs(self, *paths): # Create Dir with over and sub dir
        """Create The Directorys, with all Over and Sub Directorys

        Args:
            *paths (str):
                The Paths which you want create.
        """
        for path in paths: # Create Slife for all paths
            if self.operating_platform == 'Linux': # Command for Linux
                command = f"mkdir -p {path}"
            elif self.operating_platform == 'Windows': # Command for Windows
                command = f"mkdir {path}"
            else: # If the Platform not Linux or Windows
                print("Invalid Platform")
                sys.exit(1)
            self.run(command) # Execute the Command

    def copy(self, *files, target): # Command for Copy Things
        """Copy Files and Directorys to the target

        Args:
            *files (str):
                The Files and Directorys which you want Copy.
            target (str):
                The Target Directory.
        """
        for file in files: # Create Slife
            if self.operating_platform == 'Linux': # Command for Linux
                command = f"cp -rf {file} {target}"
            elif self.operating_platform == 'Windows': # Command for Windows
                command = f"copy /y {file} {target}"
            else: # If not Linux or Windows
                print("Invalid Platform")
                sys.exit(1)
            self.run(command) # Execute the Command

    def remove(self, *files): # Command to Remove Files and Directorys
        """Remove Files and Directorys
        
        Args:
            *files (str):
                The Files or Directorys which you want Remove.
        """
        for file in files: # Create Slife
            if self.operating_platform == 'Linux': # Command for Linux
                command = f"rm -rf {file}"
            elif self.operating_platform == 'Windows': # Command for Windows
                command = f"del /f /s /q {file}"
            else: # If not Linux or Windows
                print("Invalid Platform")
                sys.exit(1)
            self.run(command)

    def move(self, *files, target): # Command to Move files to target
        """Move Files or Directorys to the Target
        
        Args:
            *files (str):
                The Files or Directorys.
        """
        for file in files:
            if self.operating_platform == 'Linux': # Command for Linux
                command = f"mv {file} {target}"
            elif self.operating_platform == 'Windows': # Command for Windows
                command = f"move {file} {target}"
            else: # If not Linux or Windows
                print("Invalid Platform")
                sys.exit(1)
            self.run(command)

    def rename(self, old_name, new_name):
        """Rename The File/Directory

        Args:
            old_name (str):
                The Old Name (What have you thought).
            new_name (str):
                The New Name (Surprise, Surprise).
        """
        if self.operating_platform == 'Linux': # Command for Linux
            command = f"mv {old_name} {new_name}"
        elif self.operating_platform == 'Windows': # Command for Windows
            command = f"ren {old_name} {new_name}"
        else: # If not Linux or Windows
            print("Invalid Platform")
            sys.exit(1)
        self.run(command)

    def listdir(self, path):
        """Show the Files and Directory in the given Path
        
        Args:
            path (str):
                The Path.
        """
        if self.operating_platform == 'Linux': # Command for Linux
            command = f"ls {path}"
        elif self.operating_platform == 'Windows': # Command for Windows
            command = f"dir {path}"
        else: # If not Linux or Windows
            print("Invalid Platform")
            sys.exit(1)
        self.run(command)

    def clear(self): # Clear the Terminal
        """Clear The Terminal"""
        if self.operating_platform == 'Linux': # Command for Linux
            command = "clear"
        elif self.operating_platform == 'Windows': # Command for Windows
            command = "cls"
        else: # If not Linux or Windows
            print("Invalid Platform")
            sys.exit(1)
        self.run(command)

    def changedir(self, path): # Change the Workdir
        """Change The Workdir

        Args:
            path (str):
                The New Workdir
        """
        if self.operating_platform == 'Linux': # Command Linux
            command = f"cd {path}"
        elif self.operating_platform == 'Windows': # Command Windows
            command = f"cd {path}"
        else: # If not Linux or Windows
            print("Invalid Platform")
            sys.exit(1)
        self.run(command)

class Download:
    """Class To Download Files"""
    def __init__(self, client, operating_platform):
        """Init your Client

        Args:
            client (str):
                Set Your Client ('curl', 'wget')
            operating_platform (str):
                Set the Platform ('Linux', 'Windows')
        """
        self.client = client
        self.operating_platform = operating_platform

    def file_original_name(self, url): # Download a File
        """Download A File

        Args:
            url (str):
                The Download Url
        """
        if self.operating_platform == 'Linux':
            system = System("Linux")
        elif self.operating_platform == 'Windows':
            system = System("Windows")
        else:
            print("Invalid Platform")
            sys.exit(1)

        if self.client in ["curl", "Curl"]:
            command = f"curl -OL {url}"
        elif self.client in ["wget", "Wget"]:
            command = f"wget {url}"
        else:
            print("Invalid Client")
            sys.exit(1)
        system.run(command)

    def file_set_name_in_this_path(self, url, name):
        """Download a File and give a Name, safe this in actual Path
        
        Args:
            url (str):
                The Download URL
            name (str):
                The Name
        """
        if not self.operating_platform in ["Linux", "Windows"]:
            print("Invalid Platform")
            sys.exit(1)
        else:
            system = System(self.operating_platform)

        if self.client in ["curl", "Curl"]:
            command = f"curl -o {name} -L {url}"
        elif self.client in ["wget", "Wget"]:
            command = f"wget -o {name} {url}"
        else:
            print("Invalid Client")
            sys.exit(1)
        system.run(command)

    def file_set_name_in_other_path(self, url, name, path):
        """Download Path and Give a Name, Safe this in an other path

        Args:
            url (str):
                The Download Url
            name (str):
                The New File Name
            path (str):
                The Safe Path
        """
        full_path = f"{path}/{name}"
        if not self.operating_platform in ["Linux", "Windows"]:
            print("Invalid Platform")
            sys.exit(1)
        else:
            system = System(self.operating_platform)
        
        if self.client in ["curl", "Curl"]:
            command = f"curl -o {full_path} -L {url}"
        elif self.client in ["wget", "Wget"]:
            command = f"wget -o {full_path} {url}"
        else:
            print("Invalid Client")
            sys.exit(1)
        system.run(command)

class Manipulate:
    """Class To Manipulate Terminal Output"""

    def __init__(self, operating_platform):
        """Initial the Class
        
        Args:
            operating_platform (str):
                The Base System ('Linux', 'Windwos')
        """
        self.operating_platform = operating_platform

    def draft(self, x, y):
        """Set Positiom by x, y

        Args:
            x (int):
                X Coordinate
            y (int):
                y Coordinate
        """
        if not self.operating_platform in ["Linux", "Windows"]:
            print("Invalid Platform")
            sys.exit(1)
        else:
            system = System(self.operating_platform)

        if self.operating_platform == 'Linux':
            command = f"tput cup {x} {y}"
        elif self.operating_platform == 'Windows':
            command = f"setxy {x} {y}"
        system.run(command)

    def print(self, x, y, content):
        """Print a Message on Given Position

        Args:
            x (int):
                x Coordinates
            y (int):
                y Coordinates
            content (str):
                Content (Text)
        """
        if not self.operating_platform in ["Linux", "Windows"]:
            print("Invalid Platform")
            sys.exit(1)

        self.draft(x, y)
        print(content)

    def input(self, x, y, prompt):
        """Set a Input on Given Position

        Args:
            x (int):
                x Coordinates
            y (int):
                y Coordinates
            prompt (str):
                Input Prompt
        """
        if not self.operating_platform in ["Linux", "Windows"]:
            print("Invalid Platform")
            sys.exit(1)

        self.draft(x, y)
        input(prompt)

    def clear_screen(self, type):
        """Clear the Screen by Given Type

        Args:
            type={type}:
                With type options ['clear', 'reset', 'init']
        """
        if not self.operating_platform in ["Linux", "Windows"]:
            print("Invalid Platform")
            sys.exit(1)
        else:
            system = System(self.operating_platform)

        if type == 'clear':
            if self.operating_platform == 'Linux':
                command = "tput clear"
            elif self.operating_platform == 'Windows':
                command = "cls"
        elif type == 'reset':
            if self.operating_platform == 'Linux':
                command = "tput reset"
            elif self.operating_platform == 'Windows':
                command = "cls"
        elif type == 'init':
            if self.operating_platform == 'Linux':
                command = "tput init"
            elif self.operating_platform == 'Windows':
                command = "cls"
        else:
            print("Invalid Type")
            sys.exit(1)
        system.run(command)

    def move_cursor(self, type):
        """Move Cursor 1 Postion up, downl, right or left
        
        Args:
            type={type}:
                With type ['up', 'down', 'right', 'left']
        """
        if not self.operating_platform in ["Linux", "Windows"]:
            print("Invalid Platform")
            sys.exit(1)
        else:
            system = System(self.operating_platform)

        if type == 'up':
            if self.operating_platform == 'Linux':
                command = "tput cuu1"
            elif self.operating_platform == 'Windows':
                command = "echo -ne '\e[A'"
        elif type == 'down':
            if self.operating_platform == 'Linux':
                command = "tput cud1"
            elif self.operating_platform == 'Windows':
                command = "echo -ne '\e[B'"
        elif type == 'right':
            if self.operating_platform == 'Linux':
                command = "tput cuf1"
            elif self.operating_platform == 'Windows':
                command = "echo -ne '\e[C'"
        elif type == 'left':
            if self.operating_platform == 'Linux':
                command = "tput cub1"
            elif self.operating_platform == 'Windows':
                command = "echo -ne '\[D'"
        else:
            print("Invalid Type")
            sys.exit(1)

    def keyboard(self, key, position):
        """Use Keyboard in Python

        Args:
            key={key}:
                With key ['backspace', 'delete_full', 'screen_from', 'delete_to, 'lines_add', 'lines_del', 'delete_from', 'set_hor', 'set_ver']
            position (int):
                Give the Position (Not needed for Backspace, delete_full, screen_from)
        """
        if not self.operating_platform in ["Linux", "Windows"]:
            print("Invalid Platform")
            sys.exit(1)
        else:
            system = System(self.operating_platform)

        if key == 'backspace':
            if self.operating_platform == 'Linux':
                command = "tput kbs"
            elif self.operating_platform == 'Windows':
                command = "echo -ne ''\b"
        elif key == 'delete_full':
            if self.operating_platform == 'Linux':
                command = "tput el"
            elif self.operating_platform == 'Windows':
                command = "echo -ne '\e[K'"
        elif key == 'screen_from':
            if self.operating_platform == 'Linux':
                command = "tput ed"
            elif self.operating_platform == 'Windows':
                command = "echo -ne '\e[J'"
        elif key == 'delete_to':
            if self.operating_platform == 'Linux':
                command = "tput el1"
            elif self.operating_platform == 'Windows':
                command = "echo -ne '\e[1K'"
        elif key == 'delete_from':
            if self.operating_platform == 'Linux':
                command = f"tput ech {position}"
            elif self.operating_platform == 'Windows':
                command = f"echo -ne '\e[X{position}'"
        elif key == 'lines_add':
            if self.operating_platform == 'Linux':
                command = f"tput il {position}"
            elif self.operating_platform == 'Windows':
                command = f"echo -ne '\e[{position}L'"
        elif key == 'lines_del':
            if self.operating_platform == 'Linux':
                command = f"tput dl {position}"
            elif self.operating_platform == 'Windows':
                command = f"echo -ne '\e[{position}M'"
        elif key == 'set_hor':
            if self.operating_platform == 'Linux':
                command = f"tput hpa {position}"
            elif self.operating_platform == 'Windows':
                command = f"echo -ne '\e[{position}G'"
        elif key == 'set_ver':
            if self.operating_platform == 'Linux':
                command = f"tput vpa {position}"
            elif self.operating_platform == 'Windows':
                command = f"echo -ne '\e[{position}d'"
        else:
            print("Invalid Key")
            sys.exit(1)