# swiss-webcam-scraper

Script that Scrapes the latest Roundshot Image

## Quickstart

1. create & establish conda/virtual environment
    ```shell
    # conda
    conda create -n sws python=3.8
    source/conda activate sws
    # venv
    py -m venv .env
    source .env/Scripts/activate
    ```
2. `pip install -r requirements.txt`
3. `python demo.py`

## How-to

```
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
```


