#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# =============================================================================
"""
@Author        :   Yujie He
@File          :   get_data_json.py
@Date created  :   2021/12/27
@Maintainer    :   Yujie He
@Email         :   yujie.he@epfl.ch
"""
# =============================================================================
"""
The module provides method to extract info from roundshot requests and write
the data into json files
"""
# =============================================================================
"""
TODO:
1. determine city/canton using geopy (https://stackoverflow.com/a/34771394)
"""
# =============================================================================

import os
import json
import time
import requests
import urllib.request

curr_dir_path = os.path.dirname(os.path.abspath(__file__))
headers = {
    "Referer": "https://www.roundshot.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
}


def swiss_language_convert():
    """
    \u00e2 -> â (Château) -> a
    \u00e9 -> é (Aéroport) -> e
    \u00e8 -> è (Belvedère) -> e
    \u00f4 -> ô (Dôle) o

    \u00e4 -> ä (Alp Stätz) -> a
    \u00f6 -> ö (Schönegg Hotel) -> o
    \u00fc -> ü (Zürich) -> u
    """
    pass


# packets from 'https://www.roundshot.com/xml_1/internet/en/application/d170/f172.cfm'


def get_cam_loc(save_json=False):
    cam_loc_url = (
        'https://backend.roundshot.com/embedded/map/203?callback=callback971781'
    )
    cam_loc_response = requests.get(cam_loc_url, headers=headers)
    json_string = cam_loc_response.text
    json_string = json_string[json_string.find('{') : -2]  # json_string.rfind('}')
    cam_loc_json = json.loads(json_string)
    if save_json:
        with open(
            os.path.join(curr_dir_path, 'cam_loc.json'), "w"
        ) as cam_loc_json_file:
            json.dump(cam_loc_json, cam_loc_json_file, indent=4, sort_keys=False)
    return cam_loc_json


def get_cam_frame(save_json=False):
    frame_url = 'https://backend.roundshot.com/schema_list/203/frame.json'
    frame_response = requests.get(frame_url, headers=headers)

    cam_info_json = json.loads(frame_response.text)
    if save_json:
        with open(
            os.path.join(curr_dir_path, 'cam_info.json'), "w"
        ) as cam_info_json_file:
            json.dump(cam_info_json, cam_info_json_file, indent=4, sort_keys=False)
    return cam_info_json


if __name__ == "__main__":
    get_cam_loc(save_json=True)
    get_cam_frame(save_json=True)
