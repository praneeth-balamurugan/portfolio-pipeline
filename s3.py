import boto3
import os
import json

# Configure AWS S3 client
s3_client = boto3.client('s3')

# Define bucket name and local directory
bucket_name = 'your-portfolio-bucket-name'
local_directory = 'path/to/your/portfolio/files'

# Create S3 bucket
s3_client.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={'LocationConstraint': 'us-east-1'}
)

# Enable static website hosting
website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}
s3_client.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration=website_configuration
)

# Set bucket policy to make the contents public
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

# Upload files to S3 bucket
def upload_files(local_directory, bucket_name):
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = relative_path.replace("\\", "/")
            s3_client.upload_file(local_path, bucket_name, s3_path)
            print(f'Uploaded {s3_path} to {bucket_name}')

# Execute the file upload
upload_files(local_directory, bucket_name)

print("Website hosted successfully!")
print(f"Visit http://{bucket_name}.s3-website-us-east-1.amazonaws.com")
