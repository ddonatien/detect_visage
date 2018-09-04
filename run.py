"""
Interface console/detecteur
Usage : python -m detect_visage.run -h
"""
import getopt
import sys
import pika
from detect_visage.app.detect import DetectVisage


def usage():
    print(
        "python -m detect_visage.run -i <chemin_vers_image> -r <cle_de_routage>"
    )
    print("ou")
    print(
        "python -m detect_visage.run --image <chemin_vers_image> --rkey <cle_de_routage>"
    )


def callback(ch, method, properties, body):
    print("recieving : " + properties.reply_to)
    if detecteur.detect(body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        publish("Visage detecte !", ch, method, properties)
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        publish("Pas de visage", ch, method, properties)


def publish(message, ch, method, props):
    print("replying")
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(message))


try:
    opts, args = getopt.getopt(sys.argv[1:], 'h:i:r:',
                               ['help', 'image', 'rkey'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

detecteur = DetectVisage()
chemin_image = ''
routing_key = ''
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(1)
    elif opt in ('-i', '--image'):
        chemin_image = arg
    elif opt in ('-r', '--rkey'):
        routing_key = arg

if routing_key:
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='visage', exchange_type='direct')

    result = channel.queue_declare()
    queue_name = result.method.queue
    print("Input queue : %s " % queue_name)
    channel.queue_bind(
        exchange='visage', queue=queue_name, routing_key=routing_key)
    channel.basic_consume(callback, queue=queue_name)

    channel.start_consuming()

if chemin_image:
    if detecteur.detect(chemin_image):
        print("Visage detecte !")
    else:
        print("Pas de visage")
