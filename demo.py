#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# =============================================================================
"""
usage: demo.py [-h] [-o OUTPUT_FOLDER] [-w WEBCAM] [-q {0,1,2,3,4}] [-b BEGIN] [-e END]
               [-i INTERVAL]

swiss-webcam-scraper

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FOLDER, --output_folder OUTPUT_FOLDER
                        (str) if None, will write the images to current disk
  -w WEBCAM, --webcam WEBCAM
                        (str) Webcam name
  -q {0,1,2,3,4}, --quality {0,1,2,3,4}
                        (int) Quality of the Image (full, default, half, quarter, thumbnail)
  -b BEGIN, --begin BEGIN
                        (str) First image you want to download (hh-mm) or (YYYY-MM-DD_hh-mm)
  -e END, --end END     (str) Last image you want to download (hh-mm) or (YYYY-MM-DD_hh-mm)
  -i INTERVAL, --interval INTERVAL
                        (int) Interval in minute steps (min. 10 min, and can only be increased in
                        10 min steps)
"""
# =============================================================================

import os
import json
from typing import List
from datetime import datetime, timedelta

import argparse  # from docopt import docopt

from scraper.request import create_url, ThreadedFetcher

# load webcam dict
curr_dir_path = os.path.dirname(os.path.abspath(__file__))
webcam_json_path = os.path.join(curr_dir_path, 'json', 'swiss_webcams.json')
with open(webcam_json_path, 'r') as webcam_json:
    WEBCAMS = json.load(webcam_json)

# image quality (not every image has `_eight` suffix)
QUALITIES = {0: 'full', 1: 'default', 2: 'half', 3: 'quarter', 4: 'thumbnail'}

# datetime format
short_time_format = '%H-%M'
time_format = '%Y-%m-%d_%H-%M'


def main():
    # argument parsing
    parser = argparse.ArgumentParser(description="swiss-webcam-scraper")
    parser.add_argument(
        "-o",
        "--output_folder",
        default=os.path.join(curr_dir_path, 'data'),
        type=str,
        help="(str) if None, will write the images to current disk",
    )
    parser.add_argument(
        "-w",
        "--webcam",
        default='wildspitz',
        type=str,
        help="(str) Webcam name",
    )
    parser.add_argument(
        "-q",
        "--quality",
        default=1,
        type=int,
        choices=[0, 1, 2, 3, 4],
        help="(int) Quality of the Image (full, default, half, quarter, thumbnail)",
    )
    parser.add_argument(
        "-b",
        "--begin",
        type=str,
        help="(str) First image you want to download (hh-mm) or (YYYY-MM-DD_hh-mm)",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=str,
        help="(str) Last image you want to download (hh-mm) or (YYYY-MM-DD_hh-mm)",
    )
    parser.add_argument(
        "-i",
        "--interval",
        default=10,
        type=int,
        help="(int) Interval in minute steps (min. 10 min, and can only be increased in 10 min steps)",
    )
    args = parser.parse_args()

    start_time = end_time = datetime.now()
    if args.begin:
        try:
            if len(args.begin) > 5:
                start_time = datetime.strptime(args.begin, time_format)
            else:
                new_time = datetime.strptime(args.begin, short_time_format)
                start_time = start_time.replace(
                    hour=new_time.hour, minute=new_time.minute
                )
                # should by default only download one image
                end_time = start_time
        except ValueError:
            print('Start parameter did not contain correct date format')

    if args.end:
        try:
            if len(args.end) > 5:
                end_time = datetime.strptime(args.end, time_format)
            else:
                new_time = datetime.strptime(args.end, short_time_format)
                end_time = end_time.replace(hour=new_time.hour, minute=new_time.minute)
        except ValueError:
            print('End parameter did not contain correct date format')

    # interval
    interval = int(args.interval)
    if interval == 0:
        raise ValueError('Interval must at least be 10 minutes')
    elif interval % 10 > 0:
        raise ValueError('Interval can only be a value divisible by 10')

    # webcam
    webcam_name = str(args.webcam.lower())
    if webcam_name not in WEBCAMS:
        raise ValueError('No valid Webcam was selected')
    webcam_link = WEBCAMS[webcam_name]

    # quality ('default')
    quality = QUALITIES[args.quality]

    start_time = start_time.replace(
        minute=start_time.minute - (start_time.minute % 10), second=0, microsecond=0
    )

    print("# output_folder:", args.output_folder)
    print("# webcam_name:", webcam_name)
    print("# webcam_link:", webcam_link)
    print("# quality:", quality)
    print("# start_time:", start_time)
    print("# end_time:", end_time)
    print("# interval:", interval)

    # max 3 threads at a time
    active_threads: List = []
    while start_time < end_time:
        if len(active_threads) < 3:
            t = ThreadedFetcher(
                create_url(webcam_link, start_time, quality),
                start_time,
                webcam_name,
                args.output_folder,
            )
            t.start()
            start_time += timedelta(minutes=interval)
            active_threads.append(t)
        else:
            active_threads[0].join()
            active_threads.pop(0)


if __name__ == '__main__':
    main()
