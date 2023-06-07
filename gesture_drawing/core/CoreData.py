import time
import os 
import re 
from typing import Union



def find_files(folder: str, include_subdirs:bool=True, name_matches:re.Pattern=None, output_list:list[str]=None):

    if output_list is None:
        output_list = []

    for i in os.listdir(folder):

        path = os.path.join(folder, i)

        if os.path.isfile(path):

            if name_matches and not name_matches.match(i):
                continue

            output_list.append(path)

        elif include_subdirs:

            find_files(path, include_subdirs, name_matches, output_list)

    return output_list


def count_files_and_folders(directory: str, include_subdirs=True, name_matches:re.Pattern=None):

    file_count = 0
    folder_count = 0
    for i in os.listdir(directory):

        if not os.path.isdir(i):

            if name_matches and not name_matches.match(i):
                continue

            file_count += 1

        elif include_subdirs:

            fc, df = count_files_and_folders(os.path.join(directory, i), True)

            file_count += fc 
            folder_count += df + 1

    return file_count, folder_count





def time_now() -> int:
    return int(time.time())


def time_now_float() -> float:
    return time.time()


def time_now_precise() -> float:
    return time.perf_counter()


def time_has_passed(timestamp: Union[float, int]) -> bool:
    if timestamp is None:
        return False

    return time_now() > timestamp


def time_has_passed_float(timestamp: Union[float, int]) -> bool:
    return time_now_float() > timestamp


def time_has_passed_precise(precise_timestamp: Union[float, int]) -> bool:
    return time_now_precise() > precise_timestamp


def time_until(timestamp: Union[float, int]) -> Union[float, int]:
    return timestamp - time_now()


def time_delta_since_time(timestamp):
    time_since = timestamp - time_now()

    result = min(time_since, 0)

    return -result


def time_delta_until_time(timestamp):
    time_remaining = timestamp - time_now()

    return max(time_remaining, 0)


def time_delta_until_time_float(timestamp):
    time_remaining = timestamp - time_now_float()

    return max(time_remaining, 0.0)


def time_delta_until_time_precise(t):
    time_remaining = t - time_now_precise()

    return max(time_remaining, 0.0)




