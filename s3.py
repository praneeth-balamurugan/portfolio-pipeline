import boto3
import os
import json
import mimetypes

# Configure AWS S3 client
s3_client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='AKIAR5T2GA3NFVJPCOHW',
    aws_secret_access_key='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'
)

# Define bucket name and local directory
bucket_name = 'bp-portfolio'
local_directory = r'D:\portfolio-pipeline'

def create_bucket(bucket_name):
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket {bucket_name} already exists and is owned by you.")
    except Exception as e:
        print(f"Error creating bucket: {e}")

def enable_website_hosting(bucket_name):
    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
    }
    s3_client.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration=website_configuration
    )
    print("Static website hosting enabled.")

def set_bucket_policy(bucket_name):
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }]
    }

    bucket_policy_json = json.dumps(bucket_policy)
    s3_client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=bucket_policy_json
    )
    print("Bucket policy set.")

def upload_files(local_directory, bucket_name):
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = relative_path.replace("\\", "/")
            content_type, _ = mimetypes.guess_type(local_path)
            content_type = content_type if content_type else 'application/octet-stream'
            s3_client.upload_file(
                local_path, bucket_name, s3_path,
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': 'max-age=3600'  # Adjust max-age as needed
                }
            )
            print(f'Uploaded {s3_path} to {bucket_name} with content type {content_type}')

if __name__ == "__main__":
    create_bucket(bucket_name)
    enable_website_hosting(bucket_name)
    set_bucket_policy(bucket_name)
    upload_files(local_directory, bucket_name)
    print("Website hosted successfully!")
    print(f"Visit http://{bucket_name}.s3-website-us-east-1.amazonaws.com")
    print("object link https://bp-portfolio.s3.amazonaws.com/index.html")
