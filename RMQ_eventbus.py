import random
import pika
import json
from dataclasses import dataclass
from typing import Dict, Any

class RabbitMQEventBus:

    def __init__(self, host='localhost', username='user', password='password'):
        """Initialize RabbitMQ connection and channel"""
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, credentials=credentials))
        self.channel = self.connection.channel()
        print('RMQ Channel Established')

        # Declare main exchange
        self.channel.exchange_declare(
            exchange='main_event_exchange', 
            exchange_type='headers'
        )
        print('main_event_exchange Established')

        # Declare dead-letter exchange
        self.channel.exchange_declare(
            exchange='deadletter_exchange', 
            exchange_type='fanout'
        )
        print('deadletter_exchange Established')


    def create_consumer_queue(self, consumer_name: str, event_types: list):
        """Create a consumer-specific queue with dead-lettering exchange"""
        # Declare queue with dead-letter configuration
        queue_name = f'{consumer_name}_queue'
        self.channel.queue_declare(
            queue=queue_name,
            arguments={
                'x-dead-letter-exchange': 'deadletter_exchange'
            }
        )

        # Bind queue to main exchange with headers matching event types
        for event_type in event_types:
            self.channel.queue_bind(
                exchange='main_event_exchange',
                queue=queue_name,
                arguments={'x-match': 'any', 'event_type': event_type}
            )

        print(f"{queue_name} created and bound to main_event_exchange")
        return queue_name


    def publish_event(self, event_type: str, payload: Dict[str, Any]):
        """Publish an event to the main exchange"""
        headers = {
            'event_type': event_type
        }
        
        self.channel.basic_publish(
            exchange='main_event_exchange',
            routing_key='',
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                headers=headers,
                delivery_mode=2  # Make message persistent
            )
        )
        print(f"Event Published: {event_type}: {payload}")


    def consume_events(self, queue_name: str, callback: callable):
        """Consume events from a specific queue"""
        self.channel.basic_consume(
            queue=queue_name, 
            on_message_callback=callback,
            auto_ack=True
        )
        self.channel.start_consuming()

