import os
import boto3, json
import time

# ENV VARs
AVAILABILITY_LAMBDA_ARN = os.environ['AVAILABILITY_LAMBDA_ARN']
APP_URL = os.environ['APP_URL']

__author__ = "ssengott@"
def lambda_handler(event, context):

    print("trigger load lambda.")
    print(event)

    start_time = time.time()

    try:
        print("invoking avail_lambda asynchronously")
        # invoke availability lambda asynchronously
        lambda_client = boto3.client('lambda')
        payload = {"app_url": APP_URL}
        msg = json.dumps(payload)
        resp = lambda_client.invoke(FunctionName=AVAILABILITY_LAMBDA_ARN,
                                    InvocationType='Event',
                                    Payload=msg)
        print("async availability_lambda invoke response=" + str(resp))
    except Exception as exc:
        print("****GD: Exception when invoking availability_lambda:" + str(exc))

    end_time = time.time()
    print(f"Runtime of this trigger is: {end_time - start_time}")

    print("completed.")