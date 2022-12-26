import os
import sys
import json
import pika
import inspect

isPI = os.uname()[4][:3] == 'arm'

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config import NLED

try:
    import board
    import neopixel
except ImportError:
    if isPI:
        print('[❌] import error for neopixel')

if isPI:
    pixels = neopixel.NeoPixel(board.D18, NLED, brightness=0.25,
                               pixel_order=neopixel.RGB, auto_write=False)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='neopixel')

    def onMessage(ch, method, properties, body):
        dad_bod = json.loads(body)
        if 'array' in dad_bod:
            colors = dad_bod['array']
            if isPI:
                for i in range(len(coylors)):
                    c =  colors[i]
                    pixels[i] = (c[0], c[1], c[2])
                pixels.show()
        elif 'script' in dad_bod:
            script = dad_bod['script']
            print('script!', script)
            pass

    channel.basic_consume(queue='neopixel',
                          auto_ack=True,
                          on_message_callback=onMessage)

    print('[*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)



# To run as a systemd service
# /etc/systemd/system/neopixel.service

'''
[Unit]
Description=Neopixel IOT service
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /var/www/xmas-iotree/workers/neopixels.py

[Install]
WantedBy=multi-user.target
'''
# sudo systemctl daemon-reload
# sudo systemctl enable neopixel.service
# sudo systemctl start neopixel.service
