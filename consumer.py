import threading
import json
from RMQ_eventbus import RabbitMQEventBus
from utils import *


# Call backs to handle events
def order_service_consumer(ch, method, properties, body):
    eventbody = json.loads(body)
    event_type = properties.headers['event_type']
    print(f"Order Service Received: {event_type} : {eventbody}")
    # Process order event

def inventory_service_consumer(ch, method, properties, body):
    eventbody = json.loads(body)
    event_type = properties.headers['event_type']
    print(f"Inventory Service Received: {event_type} : {eventbody}")
    # Process inventory event


# Create worker/consumer thread using this function. 
def consumer_service(queue_name:str, callback:callable):
    # each thread needs its own instance of the event bus
    event_bus = RabbitMQEventBus()  
    event_bus.consume_events(queue_name, callback)

# ========================================================
def main():

    # # Consume events from a single queue in a non-thread manner [for debugging]
    # consumer_service('order_service_queue', order_service_consumer)


    # Run order service consumer in a separate thread
    order_thread = threading.Thread(
        target=consumer_service, args=('order_service_queue', order_service_consumer)
    )
    order_thread.start()

    # Run inventory service consumer in a separate thread
    inventory_thread = threading.Thread(
        target=consumer_service, args=('inventory_service_queue', inventory_service_consumer)
    )
    inventory_thread.start()


    # Join threads to ensure they keep running
    order_thread.join()
    inventory_thread.join()





if __name__ == '__main__':
    main()
