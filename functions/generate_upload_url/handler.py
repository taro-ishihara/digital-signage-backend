import os
import json
import boto3
import logging
import uuid

s3_client = boto3.client('s3')

logger = logging.getLogger()
level_name = os.environ['LOG_LEVEL']
level = logging.getLevelName(level_name)
logger.setLevel(level)

def lambda_handler(event, context):
    request_body = event['body']
    json_request_body = json.loads(request_body)
    prefix = json_request_body['prefix']
    content_type = json_request_body['content_type']
    
    file_name = str(uuid.uuid4())
    file_name = '{}.{}'.format(file_name, content_type.split('/')[1])
    object_key = os.path.join(prefix, file_name)
    logger.info("Object Key: {} Content Type: {}".format(object_key, content_type))
    
    upload_url = s3_client.generate_presigned_url(
        ClientMethod = 'put_object',
        Params = {
            'Bucket': os.environ['CONTENTS_BUCKET_NAME'],
            'Key': object_key,
            'ContentType': content_type
        },
        ExpiresIn = 300,
        HttpMethod = 'PUT'
    )

    return {
        'uploadUrl': upload_url
    }
