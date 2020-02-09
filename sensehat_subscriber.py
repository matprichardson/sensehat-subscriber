from google.cloud import pubsub_v1
from sense_hat import SenseHat
import ast # Use this to convert text based list to an actual one

project_id = "wagstaffe-nodeapp"
subscription_name = "get-led-config-pull"
timeout = 1200.0  # "How long the subscriber should listen for
# messages in seconds"

sense = SenseHat()


subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_name}`
subscription_path = subscriber.subscription_path(
    project_id, subscription_name
)

def callback(message):
    print("Received message: {}".format(message.data))
    
    # These can be used as debug messages
    list_raw = '[' + message.data + ']'
    list_conv = ast.literal_eval(list_raw)
    
    # Set pixels on the sensehat
    sense.set_rotation(180)
    sense.set_pixels(list_conv)
    
    print("List: ", list_conv)
    print(type(list_conv))
    
    message.ack()

streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback
)

print("Listening for messages on {}..\n".format(subscription_path))

# result() in a future will block indefinitely if `timeout` is not set,
# unless an exception is encountered first.
try:
    streaming_pull_future.result(timeout=timeout)
except:  # noqa
    streaming_pull_future.cancel()