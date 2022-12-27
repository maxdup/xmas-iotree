import os
import json
import requests
import argparse


def submit_leds(config_url, filename):
    with open(filename, 'r+') as f:
        body = f.read()
    script_name = os.path.basename(filename)
    requests.post(os.path.join(
        config_url, 'api/script/', script_name), data=body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Submit a script to your led controller')

    parser.add_argument('url',
                        help='The api endpoint that controls your leds (ex: http://192.168.1.11).')

    parser.add_argument('script',
                        help='The .py file to use as a script (ex: myscript.py).')

    args = parser.parse_args()
    led_url = args.url
    script_file = args.script

    try:
        submit_leds(led_url, script_file)
    except Exception as e:
        print(e)
