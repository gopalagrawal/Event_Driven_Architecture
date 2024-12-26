from RMQ_eventbus import RabbitMQEventBus
from utils import *


# ========================================================
def main():
    event_bus = RabbitMQEventBus()

    # Create queues for different services
    order_queue = event_bus.create_consumer_queue(
        'order_service', 
        event_types=['order_created', 'order_updated']
    )
    
    inventory_queue = event_bus.create_consumer_queue(
        'inventory_service', 
        event_types=['stock_updated', 'product_added']
    )


    # # Publish a single event for debugging
    # event_bus.publish_event('order_created', {
    #     'order_id': str(rand(1000, 9999)),
    #     'customer_name': 'John Doe'
    # })


    # Publish events continuously
    while True:
        sleep(5, 10)

        event_bus.publish_event('order_created', {
            'order_id': str(rand(1000, 9999)),
            'customer_name': 'John Doe'
        })

        event_bus.publish_event('stock_updated', {
            'product_id': 'SKU-' + str(rand(100, 999)),
            'quantity': rand(1, 100)
        })


if __name__ == '__main__':
    main()
