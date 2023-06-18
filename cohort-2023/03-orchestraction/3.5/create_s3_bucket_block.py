from time import sleep
from prefect_aws import S3Bucket, AwsCredentials
from credentials_aws import access_key, secret_access_key



def create_aws_creds_block():
    my_aws_creds_obj = AwsCredentials(
        aws_access_key_id=access_key, aws_secret_access_key = secret_access_key
    )
    my_aws_creds_obj.save(name="my-aws-creds", overwrite=True)


def create_s3_bucket_block():
    aws_creds = AwsCredentials.load("my-aws-creds")
    my_s3_bucket_obj = S3Bucket(
        bucket_name="my-first-bucket-abc", credentials=aws_creds
    )
    my_s3_bucket_obj.save(name="s3-bucket-example", overwrite=True)


if __name__ == "__main__":
    create_aws_creds_block()
    sleep(5)
    create_s3_bucket_block()

# prefect server start
# run module.py
# prefect block type ls 
# prefect block register -m prefect_aws

# en esta parte se añadiría la creación para el block  de buket en aws
