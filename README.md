# Event_Driven_Architecture
This is a sample EDA based application with the following features:
- The RabbitMQ message broker is used. It runs as a docker container. 
- The producers and consumers are 2 separate processes.
- Multiple exchanges and event queues are used. Consumers subscribe to these event queues. 


----------------
# Running Application Components

## Step 1: Start RabbitMQ container
- `docker-compose up --detach`
- Can later shut it down gracefully with : `docker-compose down`


## Step 2: Run producer and consumers
- `python main.py`
- This starts the producer process and consumer process. 
- The producer will continuously produce random events every 5-10 seconds
- The consumer process uses threads to spin up multiple consumers.
- Each consumer creates its own instance of RabbitMQEventBus object to access RMQ
- Each consumer is constantly listening for events on the event_queues. 





