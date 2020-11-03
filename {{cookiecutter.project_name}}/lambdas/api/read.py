import json
import boto3
import os
from utils import *

dynamo = boto3.client("dynamodb")
dynamo_table = os.environ.get('DDB_TABLE_NAME', "{{cookiecutter.api_domain}}-api-ddb-table")

# Method: GET, PATH /{{cookiecutter.api_domain}}/{id} or /{{cookiecutter.api_domain}}
def handler(event, context):

    body = event.get('body')
    return {
        "statusCode": 200,
        "body": body
    }
