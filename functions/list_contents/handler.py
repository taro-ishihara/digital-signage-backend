import os
import json
import boto3
import logging

s3_client = boto3.client('s3')

logger = logging.getLogger()
level_name = os.environ['LOG_LEVEL']
level = logging.getLevelName(level_name)
logger.setLevel(level)

## S3 Client
s3_client = boto3.client('s3')

## S3 Resource
s3 = boto3.resource('s3')
contents_bucket = s3.Bucket(os.environ['CONTENTS_BUCKET_NAME'])

def lambda_handler(event, context):
    logger.info(event)
    
    prefix = event['queryStringParameters'].get('prefix', '')

    contents = contents_bucket.objects.filter(Prefix=prefix)
    filtered_contents = [{'filePath': content.key, 'etag': json.loads(content.e_tag)} for content in contents if content.key.endswith('.png') or content.key.endswith('.mp4')]

    return filtered_contents