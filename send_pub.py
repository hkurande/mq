import pika
import os
from datetime import datetime

def sendMessage(qname, message):
    try:
        if 'MQ_HOST_NAME' in os.environ:
            mqHost = os.environ['MQ_HOST_NAME']
        else:
            print('Need to define MQ hostname in env variable MQ_HOST_NAME')
            exit(2)
        connection = pika.BlockingConnection(pika.ConnectionParameters(mqHost))
        channel = connection.channel()
        #Publish/Subscribe exchange
        channel.exchange_declare(exchange='logs',
            exchange_type='fanout')
        #
        #channel.queue_declare(queue=qname)
        now = datetime.now().strftime("%b %d %Y %H:%M:%S")
        message = now + ' :' + message
        ###
        # Following for message Q
        # channel.basic_publish(exchange='',
        #     routing_key=qname,
        #     body = message)
        # Following for pub/sub
        channel.basic_publish(exchange='logs',
            routing_key='',
            body=message)
        print(now + ' Sent the message: ' + message + ', on: '+ qname)
    except:
        print('Not able to send the message ' + message + ' on '+ qname)
    
    connection.close()

for i in range(1, 10):
    myMessage = 'log message ' + str(i)
    sendMessage('log', myMessage)

print('Sent all messages')