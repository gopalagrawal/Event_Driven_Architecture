import multiprocessing
import subprocess
from utils import *

def run_producer():
    subprocess.run(['python', 'producer.py'])

def run_consumer():
    subprocess.run(['python', 'consumer.py'])


# ========================================================
if __name__ == '__main__':
    producer_process = multiprocessing.Process(target=run_producer)
    consumer_process = multiprocessing.Process(target=run_consumer)

    producer_process.start()
    sleep(2)
    consumer_process.start()

    producer_process.join()
    consumer_process.join()

    print("Main Ending")