import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/ocb3wv"
sqs = boto3.client('sqs')
# Defined a dictionary
Dict = {}


def get_message():
        try:
        # Receive message from SQS queue. Each message has two MessageAttributes: order and word
        # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ],
            )
        # Check if there is a message in the queue or not
            if "Messages" in response:
            # extract the two message attributes you want to use as variables
            # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']

            # Print the message attributes - this is what you want to work with to reassemble the message
            # Put the attributes into a dicionary and sorted it
                Dict[f'{order}'] = f'{word}'
                sortDict = list(Dict.keys())
                sortDict.sort()
                final_dict = {i: Dict[i] for i in sortDict}
 
                print(final_dict)
        # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                exit(1)
            
    # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])
    # This part deletes the message after it is put in the dictionary
        try:
            # Delete message from SQS queue
            sqs.delete_message(
                QueueUrl=url,
                ReceiptHandle=handle
            )
            print("Message deleted")
        except ClientError as e:
            print(e.response['Error']['Message'])


# Trigger the function. Adding in the while True allows it to run until the queue is empty
if __name__ == "__main__":
    while True:
        get_message()



