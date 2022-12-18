import os
import json
import pika

NLED = 50
isPI = os.uname()[4][:3] == 'arm'

try:
    import board
    import neopixel
except ImportError:
    if isPI:
        print('import error for neopixel')

if isPI:
    pixels = neopixel.NeoPixel(board.D18, NLED, brightness=0.25,
                               pixel_order=neopixel.RGB, auto_write=False)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='neopixel')

    def onMessage(ch, method, properties, body):
        colors = json.loads(body)
        if isPI:
            for p in colors:
                pixels[i] = (p[0], p[1], p[2])
            pixels.show()

        print("[!] Received %r leds" % len(colors))

    channel.basic_consume(queue='neopixel',
                          auto_ack=True,
                          on_message_callback=onMessage)

    print(' [*] Waiting for messages. To exit press CTRL+C')
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
