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
class CommandCopyFileException(CommandException):
    pass


class FileNotExistException(Exception):
    pass

class OptionException(Exception):
    pass

class ExtensionException(Exception):
    def __init__(self, extension):
        self.extension = extension

class RemoveException(Exception):
    pass


class RenameException(Exception):
    pass


class CreateException(Exception):
    pass


class CopyException(Exception):
    def __init__(self, file_name):
        self.filename = file_name


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
    def __get_parent(cls):
        path = cls.__current.split("/")
        return "/".join(path[:-1])

    @classmethod
    def __is_absolute(cls, path):
        match = r'^[a-zA-Z]:\\'
        return True if re.search(match, path) else False


    @classmethod
    def __sort_dir(cls, files: list):
        directory = list(sorted([item for item in files if os.path.isdir(cls.__path_file(item))]))
        file = list(sorted([item for item in files if item not in directory], key=lambda item: item.split(".")[1],
                           reverse=True))
        return directory + file

    @classmethod
    def __format_size(cls, value):
        ref_value = {"B": (1, 1024), "KB": (1024, 1024 ** 2),
                     "MB": (1024 ** 2, 1024 ** 3), "GB": (1024 ** 3, 1024 ** 4)}
        for unit, ref in ref_value.items():
            ref_min, ref_max = ref
            if value < ref_max:
                return f"{value // ref_min}{unit}"
        return f"{value // ref_value['GB'][0]}GB"

    @classmethod
    def __is_extension(cls, value):
        return value.startswith(".")

    @classmethod
    def __get_files_by_extension(cls, extension):
        match = rf'\.{extension}$'
        result = []
        for file in os.listdir(cls.__current):
            if re.search(match, file):
                result.append(file)
        return result

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
        if directory == "..":
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
            # print(f"You are in {cls.__current}")
            # print(f"I have those files: {os.listdir(cls.__current)}")
            for item in os.listdir(cls.__current):
                # print("I check " + cls.__path_file(item) + " : " + str(os.path.isdir(cls.__path_file(item))))
                if os.path.isdir(cls.__path_file(item)):
                    get_dir.append(item)
            # print(f"You are in {cls.__current}")
            # print(f"You want {directory} in {get_dir} : {directory in get_dir}")
            if directory not in get_dir:
                raise FileNotFoundError
            else:
                # print("Mise à jour de current : ", cls.__path_file(directory))
                cls.__current = cls.__path_file(directory)
                return directory

    @classmethod
    def __ls(cls, option):
        if not cls.__current:
            cls.__current = os.getcwd()
        get_files = cls.__sort_dir([item for item in os.listdir(cls.__current)])
        if not option:
            return "\n".join(get_files)
        else:
            if not option.startswith("-"):
                raise CommandException
            else:
                option_value = option[1:]
                get_sizes = [os.stat(cls.__path_file(item)).st_size for item in get_files]
                match option_value:
                    case "l":
                        info = [get_files[i] if os.path.isdir(get_files[i])
                                else get_files[i] + " " + str(get_sizes[i]) for i in range(len(get_files))]
                        return "\n".join(info)
                    case "lh":
                        info = [get_files[i] if os.path.isdir(get_files[i])
                                else get_files[i] + " " + cls.__format_size(get_sizes[i]) for i in
                                range(len(get_files))]
                        return "\n".join(info)
                    case _:
                        raise OptionException

    @classmethod
    def __rm(cls, files):
        if not cls.__current:
            cls.__current = os.getcwd()
        if not files:
            raise FileUnspecifiedException

        if cls.__is_extension(files):
            # We remove the "."
            extension = files[1:]
            list_by_extension = cls.__get_files_by_extension(extension)
            if list_by_extension:
                for file in list_by_extension:
                    os.remove(cls.__path_file(file))
            else:
                raise ExtensionException(files)

        else:
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
    def __mv(cls, old_name, new_name):
        if not cls.__current:
            cls.__current = os.getcwd()
        if not old_name or not new_name:
            raise CommandRenameException

        if new_name == "..":
            new_name = cls.__get_parent()

        if cls.__is_extension(old_name):
            # We remove the "."
            extension = old_name[1:]
            list_by_extension = cls.__get_files_by_extension(extension)
            print(f"You want the file with {extension}")
            print("We have : ", list_by_extension)
            if list_by_extension:
                for file in list_by_extension:
                    if os.path.exists(os.path.join(new_name, file)):
                        good_input = False
                        while not good_input:
                            choice = input(f"{file} already exists in this directory. Replace? (y/n)").lower()
                            if choice == "y":
                                good_input = True
                                os.remove(os.path.join(new_name, file))
                                shutil.move(cls.__path_file(file), cls.__path_file(new_name))
                            elif choice == "n":
                                good_input = True
                    else:
                        shutil.move(cls.__path_file(file), cls.__path_file(new_name))

            else:
                raise ExtensionException(old_name)
        else:
            if old_name not in os.listdir(cls.__current):
                raise FileNotExistException
            # case old_name is directory
            if os.path.isdir(old_name):
                if new_name in os.listdir(cls.__current):
                    raise RenameException
                else:
                    os.rename(cls.__path_file(old_name), cls.__path_file(new_name))
            # case old_name is a file
            else:
                # new_name describe a file detected by an extension
                if "." in new_name:
                    # print("I want to rename " + old_name + " to " + new_name)
                    # print("I have : ", os.listdir(cls.__current))
                    if new_name in os.listdir(cls.__current):
                        raise RenameException
                    os.rename(cls.__path_file(old_name), cls.__path_file(new_name))
                # new_name describe a directory
                else:
                    if cls.__is_absolute(new_name):
                        shutil.move(cls.__path_file(old_name), new_name)
                    else:
                        if not os.path.exists(cls.__path_file(new_name)):
                            raise FileNotExistException
                        elif new_name in os.listdir(cls.__path_file(new_name)):
                            raise RenameException
                        else:
                            shutil.move(cls.__path_file(old_name), cls.__path_file(new_name))

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
    def __cp(cls, path_file, dest_path):
        if not cls.__current:
            cls.__current = os.getcwd()
        if not path_file:
            raise CommandCopyFileException

        if dest_path == "..":
            dest_path = cls.__get_parent()

        if cls.__is_extension(path_file):
            # We remove the "."
            extension = path_file[1:]
            list_by_extension = cls.__get_files_by_extension(extension)
            if list_by_extension:
                for file in list_by_extension:
                    if os.path.exists(os.path.join(dest_path, file)):
                        good_input = False
                        while not good_input:
                            choice = input(f"{file} already exists in this directory. Replace? (y/n)").lower()
                            if choice == "y":
                                good_input = True
                                os.remove(os.path.join(dest_path, file))
                                shutil.copyfile(cls.__path_file(file), os.path.join(dest_path, file))
                            elif choice == "n":
                                good_input = True
                    else:
                        #print("You want to copy :", cls.__path_file(file), " to ", os.path.join(dest_path, file))
                        shutil.copyfile(cls.__path_file(file), os.path.join(dest_path, file))

            else:
                raise ExtensionException(path_file)

        else:
            if cls.__is_absolute(path_file) and cls.__is_absolute(dest_path):
                if not os.path.exists(path_file) or not os.path.exists(dest_path):
                    raise FileNotExistException
                # I retrieve the name of the file and check if it exists already inside de the dest_path
                file = path_file.split("\\")[-1]
                if os.path.exists(os.path.join(dest_path, file)):
                    raise CopyException(file)
                else:
                    shutil.copyfile(path_file, dest_path)
            else:
                if not os.path.exists(cls.__path_file(path_file)) or not os.path.exists(cls.__path_file(dest_path)):
                    raise FileNotExistException
                if os.path.exists(os.path.join(dest_path, path_file)):
                    raise CopyException(path_file)
                else:
                    shutil.copyfile(path_file, dest_path)


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
                        if len(arg) > 2:
                            raise ValueError
                        old, new = arg[:2]
                    except ValueError:
                        print("Specify the current name of the file or directory and the new location and/or name")
                    cls.__mv(old, new)
                case "mkdir":
                    cls.__mkdir(arg[0])
                case "cp":
                    file_path, dest_path = "", ""
                    try:
                        if len(arg) > 2:
                            raise ValueError
                        file_path, dest_path = arg[:2]
                    except ValueError:
                        print("Specify the current name of the file or directory and the new location and/or name")
                    cls.__cp(file_path, dest_path)


# run the user's program in our generated folders
os.chdir('module/root_folder')
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
        elif isinstance(e, CommandRenameException):
            print("Specify the current name of the file or directory and the new name")
        elif isinstance(e, CommandCreateException):
            print("Specify the name of the directory to be made")
        elif isinstance(e, CommandCopyFileException):
            print("Specify the file")
        else:
            print("Invalid command")
    except FileNotExistException:
        print("No such file or directory")
    except ExtensionException as e:
        print(f"File extension {e.extension} not found in this directory")
    except RenameException:
        print("The file or directory already exists")
    except CreateException as e:
        print("The directory already exists")
    except CopyException as e:
        print(f"{e.filename} already exists in this directory")
    except FileNotFoundError:
        # Exception by default, if I come here, there is problem in my exception
        FileManager.execute("ls", "")
        print("File not found")
