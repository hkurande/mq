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
#channel.queue_declare(queue='log')
# Added for pub/sub messsages
channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)
# End pub/sub

def callback(ch, method, properties, body):
    logging.info("Received %r" % body)
    #print("Received %r" % body)
# Commented out for MQ
# channel.basic_consume(queue = 'log',
#     auto_ack = True,
#     on_message_callback = callback)
# For pub/sub added
channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True
)

logging.info(' [x] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()