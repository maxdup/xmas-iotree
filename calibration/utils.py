import argparse
import json


def IOArgParser(cli_message,
                input_default=None, input_message=None,
                output_default=None, output_message=None,
                api_url=None):

    parser = argparse.ArgumentParser(description=cli_message)

    if input_default and input_message:
        parser.add_argument('-i', '--input_coords',
                            default=input_default, help=input_message)

    if output_default and output_message:
        parser.add_argument('-o', '--output_coords',
                            default=output_default, help='output_message')

    if api_url:
        parser.add_argument('-u', '--url',
                            default=None, help='The api endpoint that controls your leds (ex: http://192.168.1.11).')

    return parser.parse_args()


def JSONFileRead(input_file):
    try:
        with open(input_file, 'r+') as f:
            content = f.read() or '{}'
            coords = json.loads(content)
    except FileNotFoundError as e:
        print('Error: File "%s" could not be found' % input_file)
        exit()
    return coords


def JSONFileWrite(output_file, data):
    try:
        with open(output_file, 'w') as f:
            output = json.dumps(data)
            f.write(output)
    except FileNotFoundError as e:
        print('Error: File "%s" could not be written' % output_file)
        exit()
