import pika
import json,os

#docker
credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq", 5672, "/", credentials))
    
#local
# connection = pika.BlockingConnection(
# pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOSTNAME", "localhost"),
#                 credentials=pika.PlainCredentials(os.environ.get("RABBITMQ_USERNAME", "guest"),
#                 os.environ.get("RABBITMQ_PASSWORD", "guest"))))


channel = connection.channel()

dm_assignment1 = json.dumps({'Module':"Data_minging",'StudentID': 1234, 'answer': 'some answers, probably correct','status':'submitted'})
dm_assignment2 = json.dumps({'Module':"Data_minging",'StudentID': 1432, 'answer': 'some answers, probably correct','status':'submitted'})
cc_assignment1 = json.dumps({'Module':"Cloud_computing",'StudentID': 5678, 'answer': 'some answers, probably correct','status':'submitted'})
cc_assignment2= json.dumps({'Module':"Cloud_computing",'StudentID': 6789, 'answer': 'some answers, probably correct','status':'submitted'})
cc_assignment3 = json.dumps({'Module':"Cloud_computing",'StudentID': 6987, 'answer': 'some answers, probably correct','status':'submitted'})


#send assignment for correction
channel.basic_publish(exchange='assignment_exchange',routing_key='Data_mining_queue', body=dm_assignment1)
print("Data minging Assignment sent for correction")
channel.basic_publish(exchange='assignment_exchange',routing_key='Data_mining_queue', body=dm_assignment2)
print("Data minging Assignment sent for correction")
channel.basic_publish(exchange='assignment_exchange',routing_key='Cloud_computing_queue', body=cc_assignment1)
print("Cloud computiong Assignment sent for correction")
channel.basic_publish(exchange='assignment_exchange',routing_key='Cloud_computing_queue', body=cc_assignment2)
print("Cloud computiong Assignment sent for correction")
channel.basic_publish(exchange='assignment_exchange',routing_key='Cloud_computing_queue', body=cc_assignment3)
print("Cloud computiong Assignment sent for correction")
connection.close()

