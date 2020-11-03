import json
import boto3
import os
from utils import *

eventbridge = boto3.client("events")
dynamo = boto3.client("dynamodb")
dynamo_table = os.environ.get('DDB_TABLE_NAME', "{{cookiecutter.api_domain}}-api-ddb-table")

# Method: PUT/PATCH, Path /{{cookiecutter.api_domain}}/{id}
def handler(event, contect):

    body = event.get('body')
    return {
        "statusCode": 200,
        "body": body
    }