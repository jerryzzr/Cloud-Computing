import pika, sys, os,json


def main():
    #docker
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq", 5672, "/", credentials))
    
    #local
    # connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOSTNAME", "localhost"),
    #                 credentials=pika.PlainCredentials(os.environ.get("RABBITMQ_USERNAME", "guest"),
    #                 os.environ.get("RABBITMQ_PASSWORD", "guest"))))
    
    #credentials = pika.PlainCredentials(username='guest', password='guest')
    #parameters = pika.ConnectionParameters(host='rabbitmq', credentials=credentials)

    channel = connection.channel()

    
    def callback(ch, method, properties, body):
        assignment = json.loads(body)
        print("Received "+str(assignment['StudentID'])+","+str(assignment['status'])+","+str(assignment['Module']))
        if(assignment['status']=='corrected'):
            assignment['status']='validated'
            channel.basic_publish(exchange='assignment_exchange',routing_key='Result_queue',body=json.dumps(assignment))
        #else:
        #    channel.basic_publish(exchange='assignment_exchange',routing_key='',body=json.dumps(assignment))


        

    channel.basic_consume(queue='Validation_queue',on_message_callback=callback, auto_ack=False)

    print(' [*] Teaching assistant is Waiting...')
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