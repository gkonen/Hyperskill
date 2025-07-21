import os
import shutil
import re

class CommandException(Exception):
    pass
class FileUnspecifiedException(CommandException):
    pass
class CommandRenameException(CommandException):
    pass
class CommandCreateException(CommandException):
    pass

class OptionException(Exception):
    pass

class RemoveException(Exception):
    pass
class FileNotExistException(RemoveException):
    pass

class RenameException(Exception):
    pass

class CreateException(Exception):
    pass

class FileManager:

    COMMAND = {"pwd": [], "cd": [], "ls": ["l", "lh"],
               "rm": [], "mv": [], "mkdir": [], "cp": []}

    __current = ""

    def __init__(self):
        raise TypeError

    # region WORKING METHOD

    @classmethod
    def __path_file(cls, file):
        return os.path.join(cls.__current, file)

    @classmethod
    def __is_absolute(cls, path):
        match = r'^[a-zA-Z]:\\'
        return True if re.search(match, path) else False

    @classmethod
    def __sort_dir(cls, files: list):
        directory = list(sorted([item for item in files if os.path.isdir(cls.__path_file(item))]))
        file = list(sorted([ item for item in files if item not in directory], key=lambda item: item.split(".")[1], reverse=True ))
        return directory + file

    @classmethod
    def __format_size(cls, value):
        ref_value = { "B" : (1,1024), "KB" : (1024,1024**2),
                      "MB" : (1024**2, 1024**3) , "GB" : (1024**3, 1024**4) }
        for unit, ref in ref_value.items():
            ref_min, ref_max = ref
            if value < ref_max:
                return f"{value//ref_min}{unit}"
        return f"{value//ref_value['GB'][0]}GB"

    # endregion

    # region METHOD
    @classmethod
    def __pwd(cls):
        if cls.__current:
            return cls.__current
        else:
            os.chdir('module/root_folder')
            __current = os.getcwd()
            return os.getcwd()

    @classmethod
    def __cd(cls, directory):
        if not directory:
            raise CommandException
        # if it is the first command, it initialises the current directory
        if not cls.__current:
            cls.__current = os.getcwd()

        # get all directory of the absolute path
        list_path = cls.__current.split("\\")

        # get parent directory
        if directory == ".." :
            if len(list_path) > 2:
                cls.__current = "\\".join(list_path[:-1])
                return list_path[-2]
            # We are in the case with [ C: , root_folder] so there are no parent
            else:
                raise FileNotFoundError
        # absolute path case
        elif cls.__is_absolute(directory):
            cls.__current = directory
            return cls.__current.split("\\")[-1]
        # relative case
        else:
            get_dir = []
            print(f"You are in {cls.__current}")
            print(f"I have those files: {os.listdir(cls.__current)}")
            for item in os.listdir(cls.__current):
                # print("I check " + cls.__path_file(item) + " : " + str(os.path.isdir(cls.__path_file(item))))
                if os.path.isdir(cls.__path_file(item)):
                    get_dir.append(item)
            print(f"You are in {cls.__current}")
            print(f"You want {directory} in {get_dir} : {directory in get_dir}")
            if directory not in get_dir:
                raise FileNotFoundError
            else:
                print("Mise à jour de current : ", cls.__path_file(directory))
                cls.__current = cls.__path_file(directory)
                return directory

    @classmethod
    def __ls(cls, option):
        if not cls.__current:
            cls.__current = os.getcwd()
        get_files = cls.__sort_dir( [item for item in os.listdir(cls.__current)] )
        if not option:
            return "\n".join(get_files)
        else:
            if not option.startswith("-") :
                raise CommandException
            else:
                option_value = option[1:]
                get_sizes = [ os.stat(cls.__path_file(item)).st_size for item in get_files ]
                match option_value:
                    case "l":
                        info = [ get_files[i] if os.path.isdir(get_files[i])
                                 else get_files[i] + " " + str(get_sizes[i]) for i in range(len(get_files)) ]
                        return "\n".join(info)
                    case "lh":
                        info = [get_files[i] if os.path.isdir(get_files[i])
                                else get_files[i] + " " + cls.__format_size(get_sizes[i]) for i in range(len(get_files))]
                        return "\n".join(info)
                    case _ :
                        raise OptionException

    @classmethod
    def __rm(cls, files):
        if not cls.__current:
            cls.__current = os.getcwd()
        if not files:
            raise FileUnspecifiedException
        # We have absolute path
        if cls.__is_absolute(files):
            if not os.path.exists(files):
                raise FileNotExistException
            if os.path.isdir(files):
                shutil.rmtree(files)
            elif os.path.isfile(files):
                os.remove(files)
        # we have relative path
        else:
            if files not in os.listdir(cls.__current):
                raise FileNotExistException
            path = cls.__path_file(files)
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)

    @classmethod
    def __mv(cls, old_name, new_name ):
        if not cls.__current:
            cls.__current = os.getcwd()
        if not old_name or not new_name:
            raise CommandRenameException
        print("I want to rename " + old_name + " to " + new_name)
        print("I have : ", os.listdir(cls.__current))
        if old_name not in os.listdir(cls.__current):
            raise FileNotExistException
        if new_name in os.listdir(cls.__current):
            raise RenameException
        os.rename(cls.__path_file(old_name), cls.__path_file(new_name))

    @classmethod
    def __mkdir(cls, directory):
        if not cls.__current:
            cls.__current = os.getcwd()
        if not directory:
            raise CommandCreateException

        if cls.__is_absolute(directory):
            if os.path.exists(directory):
                raise CreateException
            else:
                os.makedirs(directory)
        else:
            print(f"You want create {directory} in {cls.__current}")
            print(f"I have those files: {os.listdir(cls.__current)}")
            print(f"Check : ", os.path.exists(cls.__path_file(directory)))
            if os.path.exists(cls.__path_file(directory)):
                raise CreateException
            else:
                os.makedirs(cls.__path_file(directory))

    @classmethod
    def __cp(cls, path_file, path_dest):
        pass

    # endregion

    @classmethod
    def execute(cls, action, *arg):
        if action not in cls.COMMAND.keys():
            raise CommandException
        else:
            match action:
                case "pwd":
                    result = cls.__pwd()
                    print(result)
                case "cd":
                    result = cls.__cd(arg[0])
                    print(result)
                case "ls":
                    result = cls.__ls(arg[0])
                    print(result)
                case "rm":
                    cls.__rm(arg[0])
                case "mv":
                    old, new = "", ""
                    try:
                        old, new = arg[:2]
                    except ValueError:
                        pass
                    cls.__mv(old, new)
                case "mkdir":
                    cls.__mkdir(arg[0])
                case "cp":
                    path_file, path_dest = "", ""
                    try:
                        path_file, path_dest = arg[:2]
                    except ValueError:
                        pass
                    cls.__cp(path_file, path_dest)

# run the user's program in our generated folders -> pout inside the class
# os.chdir('module/root_folder')
command = ""

print("Input the command")
while command != "quit":
    try:
        command = input()
        args = [""]
        if " " in command:
            command, args = command.split(" ", 1)
            args = args.split(" ")
        FileManager.execute(command, *args)
    except CommandException as e:
        if isinstance(e, FileUnspecifiedException):
            print("Specify the file or directory")
        if isinstance(e, CommandRenameException):
            print("Specify the current name of the file or directory and the new name")
        if isinstance(e, CommandCreateException):
            print("Specify the name of the directory to be made")
        else :
            print("Invalid command")

    except RemoveException as e:
        if isinstance(e, FileNotExistException):
            print("No such file or directory")

    except RenameException :
        print("The file or directory already exists")

    except CreateException as e:
        print("The directory already exists")

    except FileNotFoundError:
        # Exception by default, if I come here, there is problem in my exception
        FileManager.execute("ls","")
        print("File not found")
