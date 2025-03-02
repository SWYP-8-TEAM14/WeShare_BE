import boto3
import uuid
from django.conf import settings
import mimetypes

def upload_to_ncp_storage(image):
    """NCP Object Storage에 이미지 업로드하고 URL 반환"""
    bucket_name = settings.NCP_STORAGE_BUCKET_NAME
    file_name = f"groups/{uuid.uuid4()}_{image.name}"
    content_type = mimetypes.guess_type(image.name)[0] or "application/octet-stream"

    endpoint_url=settings.NCP_STORAGE_ENDPOINT
    aws_access_key_id=settings.NCP_ACCESS_KEY_ID
    aws_secret_access_key=settings.NCP_SECRET_ACCESS_KEY


    # s3 = boto3.resource(
    #     's3', 
    #     endpoint_url=endpoint_url,
    #     aws_access_key_id=aws_access_key_id,
    #     aws_secret_access_key=aws_secret_access_key
    # )
    # the_bucket = s3.Bucket(bucket_name)
    # the_bucket.put_object(Key=file_name, Body=image, ContentType=content_type, ACL="private")

    #########################

    session = boto3.session.Session()
    s3 = session.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    try:
        response = s3.list_buckets()
        print("성공: ", response)
    except Exception as e:
        print("실패: ", str(e))

    # s3.upload_fileobj(image, bucket_name, file_name, ExtraArgs={"ACL": "public-read", "ContentType": content_type})
    # s3.put_object_acl(ACL="public-read", Bucket=bucket_name, Key=file_name)

    return f"{endpoint_url}/{bucket_name}/{file_name}"