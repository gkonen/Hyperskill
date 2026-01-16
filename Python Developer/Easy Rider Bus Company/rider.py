import json
import string
import re

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable
from collections import Counter
from itertools import combinations, pairwise, chain
from datetime import time

test_input = """
[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "08:12"
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 5,
        "stop_type": "O",
        "a_time": "08:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": 256,
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "09:20"
    },
    {
        "bus_id": 256,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "09:45"
    },
    {
        "bus_id": 256,
        "stop_id": 6,
        "stop_name": "Abbey Road",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "09:59"
    },
    {
        "bus_id": 256,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "10:12"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "Bourbon Street",
        "next_stop": 6,
        "stop_type": "S",
        "a_time": "08:13"
    },
    {
        "bus_id": 512,
        "stop_id": 6,
        "stop_name": "Abbey Road",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:16"
    }
]
"""


#region DEFINE ENUM AND TYPE
class FieldType(Enum):
    INTEGER = "Integer"
    CHARACTER = "Character"
    STRING = "String"

class FieldName(Enum):
    BUS_ID = "bus_id"
    STOP_ID = "stop_id"
    STOP_NAME = "stop_name"
    NEXT_STOP = "next_stop"
    STOP_TYPE = "stop_type"
    A_TIME = "a_time"

class StopType(Enum):
    START = "S"
    TRANSFER = "T"
    FINISH = "F"
    ON_DEMAND = "O"

    def get_name(self):
        match self:
            case StopType.START: return "Start"
            case StopType.TRANSFER: return "Transfer"
            case StopType.FINISH: return "Finish"
            case StopType.ON_DEMAND: return "On Demand"

class ErrorType(Enum):
    REQUIRED = "required"
    TYPE = "type"
    FORMAT = "format"
    TIME = "time"

ErrorField = dict[FieldName, bool]
ReportError = dict[ErrorType, list[FieldName]]

#endregion

#region UTILITY OBJECT
@dataclass
class Field:
    name: FieldName
    required: bool
    type: FieldType


class HoursTime:

    def __init__(self, hour, minute=0):
        self.time = time(hour, minute)

    @staticmethod
    def from_string(value: str) -> "HoursTime":
        if value == "":
            return HoursTime(0, 0)
        return HoursTime(*map(int, value.split(":")))

    def __add__(self, other : "HoursTime") -> "HoursTime":
        minutes = (self.time.minute + other.time.minute) % 60
        hours = (self.time.hour + other.time.hour + (self.time.minute + other.time.minute) // 60) % 24
        return HoursTime(hours, minutes)

    def __lt__(self, other : "HoursTime"):
        return self.time < other.time

    def __gt__(self, other : "HoursTime"):
        return self.time > other.time

    def __le__(self, other : "HoursTime"):
        return self.time <= other.time

    def __ge__(self, other : "HoursTime"):
        return self.time >= other.time

    def __str__(self):
        return f"{self.time.hour:02d}:{self.time.minute:02d}"

    def __repr__(self):
        return f"HoursTime({self.time.hour}: {self.time.minute})"


@dataclass(frozen=True)
class Stop:
    id: int = field(compare=False)
    name: str
    next_stop_id: int = field(compare=False)
    type: str = field(compare=False)
    a_time: HoursTime = field(compare=False)

#endregion


class BusNetwork:

    def __init__(self, data: list[dict]):
        self.list_stop: list[Stop] = self.__extract_stop(data)
        self.network_line: dict[int, list[Stop]] = self.__extract_line(data)
        self.good_line: dict[int, bool] = {}
        self.__sort_lines()


    def __item_to_stop(self, item: dict) -> Stop:
        """
        Creates a Stop object from the given item dictionary.

        :param item: Dictionary containing stop information.
        :type item: dict
        :return: Stop object.
        :rtype: Stop
        """
        return Stop(
            id=item.get("stop_id", 0),
            name=item.get("stop_name", ""),
            next_stop_id=item.get("next_stop", 0),
            type=item.get("stop_type", ""),
            a_time=HoursTime.from_string(item.get("a_time", ""))
        )

    def __extract_stop(self, data: list[dict]) -> list[Stop]:
        """
        Extracts a list of Stop objects from the given data.

        :param data: List of dictionaries containing stop information.
        :type data: list[dict]
        :return: List of Stop objects.
        :rtype: list[Stop]
        """
        list_stop = []
        for item in data:
            list_stop.append(self.__item_to_stop(item))
        return list_stop

    def __extract_line(self, data: list[dict]) -> dict[int, list[Stop]]:
        """
        Extracts bus lines from the given data and populates the network_line attribute.

        :param data: The input data containing bus line information.
        :type data: list[dict]
        :return: A dictionary mapping bus line IDs to a list of stops on that line.
        :rtype: dict[int, list[Stop]]
        """
        line: dict[int, list[Stop]] = {}
        for item in data:
            line_id = int(item.get("bus_id", 0))
            if line_id != 0:
                new_stop = self.__item_to_stop(item)
                if line_id not in line.keys():
                    line[line_id] = [new_stop]
                else:
                    line[line_id].append(new_stop)
        return line

    def __validate_line(self):
        """
        Validates the extracted bus lines by checking if they form a valid network.
        """
        good_line = {}
        if self.network_line:
            for line_id, line in self.network_line.items():
                good_line[line_id] = self.check_line(line)

    def __sort_lines(self):
        good_line = [ line_id for line_id, is_valid in self.good_line.items() if is_valid ]
        for line_id in good_line:
            line = self.get_line_by_id(line_id)
            self.network_line[line_id] = self.__sorted_line(line)

    def __sorted_line(self, line: list[Stop]) -> list[Stop]:
        working_line = line[:]
        sorted_line = []
        start_stop = next((stop for stop in working_line if stop.type == "S"), None)
        if start_stop is None:
            return line
        working_line.remove(start_stop)

        current_stop = start_stop
        while current_stop is not None:
            sorted_line.append(current_stop)
            if current_stop in working_line:
                working_line.remove(current_stop)
            current_stop = next((stop for stop in working_line if stop.id == current_stop.next_stop_id), None)
        # In case some errors occur in stop_id, we just add the remaining stops at the ends
        if working_line:
            sorted_line.extend(working_line)

        return sorted_line

    def get_lines_id(self):
        return self.network_line.keys()

    def get_line_by_id(self, bus_id: int) -> list[Stop]:
        return self.network_line.get(bus_id, [])

    def __get_stop_by_type(self, stop_type: StopType) -> list[Stop]:
        return list(set((stop for stop in self.list_stop if stop.type == stop_type.value)))

    def get_on_demand_stop(self) -> list[Stop]:
        correct_on_demand_stop_list = []
        on_demand_stop_list = self.__get_stop_by_type(StopType.ON_DEMAND)
        start_stop_list = self.__get_stop_by_type(StopType.START)
        finish_stop_list = self.__get_stop_by_type(StopType.FINISH)
        transfer_stop_list = self.get_transfer_stop()

        for stop in on_demand_stop_list:
            if stop not in start_stop_list and stop not in finish_stop_list and stop not in transfer_stop_list:
                correct_on_demand_stop_list.append(stop)
        return correct_on_demand_stop_list


    def get_transfer_stop(self) -> list[Stop]:
        transfer_stop = []
        for line_a, line_b in combinations(self.network_line.values(), 2):
            intersection = set(line_a).intersection(set(line_b))
            transfer_stop.extend(list(intersection))

        return list(set(transfer_stop))

    def check_line(self, line: list[Stop]) -> bool:
        """Check if the line has start and end stop"""
        types = {stop.type for stop in line}
        return "S" in types and "F" in types

    def get_format_stop(self, stop_type: StopType) -> list[str]:
        match stop_type:
            case StopType.START | StopType.FINISH : return sorted(map(lambda stop: stop.name, self.__get_stop_by_type(stop_type) ))
            case StopType.ON_DEMAND : return sorted(map(lambda stop: stop.name, self.get_on_demand_stop() ))
            case StopType.TRANSFER: return sorted(map(lambda stop: stop.name, self.get_transfer_stop() ))
            case _ :
                raise ValueError(f"Invalid stop type: {stop_type}")


    def resume_network(self, debug=False):
        print("Line names and number of stops:")
        for bus_id, line  in self.network_line.items():
            print(f"bus_id: {bus_id} stops: {len(line)}")

        if not all(self.good_line.values()):
            print(f"There is no start or end stop for this line: {"".join(map(str, [bus_id for bus_id, is_good in self.good_line.items() if not is_good]))}.")
        else:
            if debug:
                print()
                for bus_id, line in self.network_line.items():
                    print(f"Line {bus_id} :")
                    self.show_line(line)
            print()
            for type_stop in StopType:
                stop_list = self.get_format_stop(type_stop)
                print(f"{type_stop.get_name()} stops: {len(stop_list)} {stop_list}")
        print()


    def show_line(self, line: list[Stop]):
        stop_name_length = 25
        for stop in line:
            print(f"{f"{stop.name} ({stop.id})":<{stop_name_length}}", end=" | ")
        print()
        print("-"*(len(line)*(stop_name_length + 3)-1))
        for stop in line:
            print(f"{f"{stop.a_time}":<{stop_name_length}}", end=" | ")
        print("\n")


class Validator:
    """
    Validator class for validating data against a set of rules and give a report of errors
    """
    def __init__(self, rule_set: list[Field]):
        self.rule_set = rule_set

    @staticmethod
    def __is_integer(value) -> bool:
        return isinstance(value, int)

    @staticmethod
    def __is_string(value) -> bool:
        return isinstance(value, str)

    @staticmethod
    def __is_character(value) -> bool:
        return isinstance(value, str) and len(value) <= 1

    @staticmethod
    def __check_format_road_name(value : str) -> bool:
        suffix = {"Road", "Avenue", "Boulevard", "Street"}
        try:
            *name_parts, suffix_name = value.rsplit(" ", 1)
            name = "".join(name_parts)
            return suffix_name in suffix and name[0] in string.ascii_uppercase
        # IndexError occurs when the string is empty
        except (ValueError, IndexError):
            return False

    @staticmethod
    def __check_format_stop_type(value : str) -> bool:
        return value in {"S", "O", "F", ""}

    @staticmethod
    def __check_format_time(value : str) -> bool:
        try:
            return re.match(r"^([0-1][0-9]|2[0-3]):([0-5][0-9])$", value) is not None
        except ValueError:
            return False

    def check_field(self, item: dict) -> ErrorField:
        """
        Provide a dictionary with a field name as a key and a boolean as a value indicating whether the field has an error
        ie must be present or not
        """
        # For the field required, if item has the keys it must be not empty, and if it has not the field, it gives an empty string
        return {
            field.name: item.get(field.name.value, "") == "" if field.required else False
            for field in self.rule_set
        }

    def check_type(self, item: dict) -> ErrorField:
        """
            Provide a dictionary with a field name as a key and a boolean as a value indicating whether the field has an error
            ie is the type correct or not
        """
        mapping = { FieldType.INTEGER: self.__is_integer,
                   FieldType.STRING: self.__is_string,
                   FieldType.CHARACTER: self.__is_character }
        return {
            field.name: not mapping[field.type](item[field.name.value]) if field.name.value in item.keys() else False
            for field in self.rule_set
        }

    def check_format(self, item: dict) -> ErrorField:
        """
            Provide a dictionary with a field name as a key and a boolean as a value indicating whether the format is correct or not
        """
        mapping = {FieldName.STOP_NAME: self.__check_format_road_name,
                   FieldName.STOP_TYPE: self.__check_format_stop_type,
                   FieldName.A_TIME: self.__check_format_time}
        return {
            field.name: not mapping[field.name](item[field.name.value]) if field.name.value in item.keys() and field.name in mapping.keys() else False
            for field in self.rule_set
        }

    def check_time(self, line: list[Stop]) -> ErrorField:
        """Check if the time is increasing for each stop"""
        stop_time = ([HoursTime(0, 0)] + [stop.a_time for stop in line])
        respect_time = [time_departure < time_arrival for time_departure, time_arrival in pairwise(stop_time)]
        return { FieldName.A_TIME : not all(respect_time) }

    def compute_format_error(self, data: list[dict]) -> list[tuple[dict, ReportError]]:
        """
        Compute the errors for all the item inside data

        :param data: List of data items to validate
        :type data: list[dict]
        :return: list of tuple of items with their errors associated
        :rtype: list[tuple[dict, ReportError]]
        """
        check_method_list: dict[ErrorType, Callable[[dict], ErrorField]] \
            = {ErrorType.REQUIRED: self.check_field,
               ErrorType.TYPE: self.check_type,
               ErrorType.FORMAT: self.check_format}

        error_list = []

        for item in data:
            # report_error give the FieldName where a given error type occurs
            report_error: ReportError = { error_name: [] for error_name in ErrorType }
            for error_type, check_method in check_method_list.items():
                error_field : ErrorField = check_method(item)
                for field_name, has_error in error_field.items():
                    if has_error:
                        report_error[error_type].append(field_name)
            error_list.append((item, report_error))

        return error_list

    def compute_network_error(self, network: BusNetwork) -> list[tuple[int, ReportError]]:
        """
        Computes the errors in the provided network's lines and returns a list of error
        reports.

        :param network: The bus network instance to evaluate for potential errors.
        :type network: BusNetwork
        :return: list of tuple of line_id with their errors associated
        :rtype: list[tuple[int, ReportError]]
        """

        error_list = []
        # For now, we have just ErrorType.TIME for the network, if further method is required, we can add them here
        # and use the same structure as ''compute_format_error''
        if network is not None:
            lines_id_list = network.get_lines_id()
            for line_id in lines_id_list:
                line = network.get_line_by_id(line_id)
                report_error: ReportError = { error_name: [] for error_name in ErrorType }

                error_time : ErrorField = self.check_time(line)
                for field_name, has_error in error_time.items():
                    if has_error:
                        report_error[ErrorType.TIME].append(field_name)
                error_list.append((line_id, report_error))
            return error_list
        else:
            return error_list

    def generate_report_error(self, data: list[dict], network: BusNetwork = None, debug=False):
        """
        Generate and report an error summary for a list of data items

        :param network: the bus network instance to evaluate for potential errors.
        :type network: BusNetwork
        :param data: List of data items to validate
        :type data: list[dict]
        :param debug: Flag to print detailed error report
        :type debug: bool
        """

        report_format = self.compute_format_error(data)
        report_network = self.compute_network_error(network)
        if debug:
            print("Format errors:")
            print(*report_format, sep="\n")
            print("Network errors:")
            print(*report_network, sep="\n")
        count_error = Counter()
        # item can be item from data or line_id from network
        for item, error in chain(report_format, report_network):
            list_error = set()
            for errors in error.values():
                list_error.update(errors)
            count_error += Counter(list_error)
        total_error = sum(count_error.values())

        print(f"Type and field validation: {total_error} errors")
        for name in FieldName:
            print(f"{name.value}: {count_error[name]}")
        print()


if __name__ == '__main__':
    debug = False
    env_dev = False
    data = test_input if env_dev else input()
    data = json.loads(data)

    rule_set = [Field(name=FieldName.BUS_ID, required=True, type=FieldType.INTEGER),
                Field(name=FieldName.STOP_ID, required=True, type=FieldType.INTEGER),
                Field(name=FieldName.STOP_NAME, required=True, type=FieldType.STRING),
                Field(name=FieldName.NEXT_STOP, required=True, type=FieldType.INTEGER),
                Field(name=FieldName.STOP_TYPE, required=False, type=FieldType.CHARACTER),
                Field(name=FieldName.A_TIME, required=True, type=FieldType.STRING)]

    bus_network = BusNetwork(data)
    Validator(rule_set).generate_report_error(data, network=bus_network, debug=debug)
    bus_network.resume_network(debug=debug)

