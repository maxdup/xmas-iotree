from utils import IOArgParser, JSONFileRead, JSONFileWrite

import os
import requests


if __name__ == '__main__':

    args = IOArgParser('Submit Coordinates to your led controller',
                       'coordinates.json',
                       'The json file containing your coordinates (ex: coordinates.json)',
                       api_url=True)

    coords = JSONFileRead(args.input_file)
    url = os.path.join(config_url, 'api/coords/')
    body = {'coords': coords}

    try:
        submit_leds(url, body)
        requests.post(url, json=body)
    except Exception as e:
        print('Network Error')
