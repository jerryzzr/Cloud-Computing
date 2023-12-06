import pika
import json,os

#docker
#credentials = pika.PlainCredentials("guest", "guest")
#connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq", 5672, "/", credentials))
    
#local
connection = pika.BlockingConnection(
pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOSTNAME", "localhost"),
                credentials=pika.PlainCredentials(os.environ.get("RABBITMQ_USERNAME", "guest"),
                os.environ.get("RABBITMQ_PASSWORD", "guest"))))


channel = connection.channel()

dm_assignment = json.dumps({'Module':"Data_minging",'StudentID': 1234, 'answer': 'some answers, probably correct','status':'submitted'})
cc_assignment = json.dumps({'Module':"Cloud_computing",'StudentID': 5678, 'answer': 'some answers, probably correct','status':'submitted'})



#send assignment for correction
channel.basic_publish(exchange='assignment_exchange',routing_key='Data_mining_queue', body=dm_assignment)
print("Data minging Assignment sent for correction")
channel.basic_publish(exchange='assignment_exchange',routing_key='Cloud_computing_queue', body=cc_assignment)
print("Cloud computiong Assignment sent for correction")
connection.close()

