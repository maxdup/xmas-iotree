import os
import json
import requests
import argparse


def submit_leds(config_url, filename):
    with open(filename, 'r+') as f:
        coords = json.loads(f.read() or '{}')
    config = {'coords': coords}
    requests.post(os.path.join(config_url, 'api/coords/'), json=config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Submit Coordinates to your led controller')

    parser.add_argument('url',
                        help='The api endpoint that controls your leds (ex: http://192.168.1.11/api/leds/).')

    parser.add_argument('-c', '--coordinates', default="coordinates.json",
                        help='The json file containing your coordinates (ex: coordinates.json).')

    args = parser.parse_args()
    led_url = args.url
    coord_file = args.coordinates

    try:
        submit_leds(led_url, coord_file)
    except Exception as e:
        print(e)
