import pika
import logging
import traceback

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
except Exception as e:
    logging.error('Could not connect to MQ Server')
    logging.error(traceback.format_exc())
    exit(2)

channel = connection.channel()
channel.queue_declare(queue='log')


def callback(ch, method, properties, body):
    logging.info("Received %r" % body)
    #print("Received %r" % body)
# Commented out for MQ
channel.basic_consume(queue = 'log',
    auto_ack = True,
    on_message_callback = callback)


logging.info(' [x] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()