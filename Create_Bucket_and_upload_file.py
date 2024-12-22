import boto3

# Initialize S3 client and resource
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

print("creating a new bucket")
bucket_name = 'buket-from-sdk'
s3_client.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': 'ap-south-1'
    }
)

print(f'Bucket {bucket_name} created successfully') 
print("uploading a file to the bucket")
file_path = 'sample.txt'

s3_client.upload_file(file_path, bucket_name ,"file.txt")
print(f'File {file_path} uploaded to {bucket_name}')
