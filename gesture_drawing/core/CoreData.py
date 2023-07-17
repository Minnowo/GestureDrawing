import logging
import time
import json
import os 
import re 
from typing import Union, MutableMapping

from . import CoreConstants as CC


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


def update_dictionary_no_key_remove(dicta: MutableMapping, dictb: MutableMapping):
    for key, value in dictb.items():
        if key in dicta and isinstance(dicta[key], MutableMapping) and isinstance(value, dict):
            update_dictionary_no_key_remove(dicta[key], value)
        else:
            dicta[key] = value


def save_json(path: str, json_:dict):

    with open(path, "w") as writer:

        json.dump(json_, writer, indent=3)

def load_json(path:str) -> dict:

    with open(path, "rb") as reader:

        return json.load(reader)

def save_settings(settings_json:dict):

    if not os.path.isdir(CC.CONFIG_DIRECTORY) and CC.CONFIG_DIRECTORY:

        os.makedirs(CC.CONFIG_DIRECTORY, exist_ok=True)


    save_json(CC.CONFIG_CLIENT_SETTINGS, settings_json)


def load_settings(settings_json:dict):

    if not os.path.isdir(CC.CONFIG_DIRECTORY) or not os.path.isfile(CC.CONFIG_CLIENT_SETTINGS):
        logging.warn("Settings file or directory does not exist")
        return

    logging.info(f"Loading settings at {CC.CONFIG_CLIENT_SETTINGS}")
    try:

        new_settings = load_json(CC.CONFIG_CLIENT_SETTINGS)
    except Exception as e:

        logging.error(e)
        return

    if not new_settings:
        logging.info("No settings loaded")
        return

    logging.info("Settings loaded successfully")

    update_dictionary_no_key_remove(settings_json, new_settings)
