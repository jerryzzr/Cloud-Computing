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
    
    channel = connection.channel()

    channel.exchange_declare(exchange='assignment_exchange',exchange_type='direct')
    channel.queue_declare(queue='Result_queue')
    channel.queue_bind(exchange='assignment_exchange',queue='Result_queue',routing_key='Result_queue')
    channel.queue_declare(queue='Cloud_computing_queue')
    channel.queue_bind(exchange='assignment_exchange',queue='Cloud_computing_queue',routing_key='Cloud_computing_queue')
    channel.queue_declare(queue='Data_mining_queue')
    channel.queue_bind(exchange='assignment_exchange',queue='Data_mining_queue',routing_key='Data_mining_queue')
    channel.queue_declare(queue='Validation_queue')
    channel.queue_bind(exchange='assignment_exchange',queue='Validation_queue',routing_key='Validation_queue')
    
    

    def callback(ch, method, properties, body):
        
        #channel.basic_publish(exchange='assignment_exchange',body='')
        assignment = json.loads(body)
        print("Received "+str(assignment['StudentID'])+","+str(assignment['Module'])+","+str(assignment['status'])+", and submit it to Brightspace")
        if(assignment['status']=='validated'):
            assignment['status']='confirmed'
        #else:
        #    channel.basic_publish(exchange='assignment_exchange',routing_key='',body=json.dumps(assignment))

    channel.basic_consume(queue='Result_queue', on_message_callback=callback, auto_ack=False)

    print(' [*] Module Coodinator is Waiting...')
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