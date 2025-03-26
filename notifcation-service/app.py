import pika
import json

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='order_events')

def callback(ch, method, properties, body):
    """
    Process incoming messages from RabbitMQ.
    """
    event = json.loads(body)
    if event['event_type'] == 'order_created':
        print(f"Sending notification for order {event['order_id']} to user {event['user_id']}")

# Subscribe to the queue
channel.basic_consume(queue='order_events', on_message_callback=callback, auto_ack=True)

if __name__ == '__main__':
    print('Notification Service is listening for events...')
    channel.start_consuming()