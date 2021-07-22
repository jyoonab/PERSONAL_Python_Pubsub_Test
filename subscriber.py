import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

credentials_path = '../data/test.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

timeout = 30.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/trans-equator-290101/subscriptions/pubsub-test-sub'

def callback(message):
    print(f'Received message: {message}')
    print(f'data: {message.data}')
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')

with subscriber:
    try:
        streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
