import boto3

# Initialize S3 client and resource
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

# Retrieve the list of existing buckets
response = s3_client.list_buckets()

# Output the bucket names and their objects
print('Existing buckets and their contents:')
for bucket in response['Buckets']:
    bucket_name = bucket['Name']
    print(f'\nBucket: {bucket_name}')
    bucket_obj = s3_resource.Bucket(bucket_name)
    
    # List all objects in the bucket
    for obj in bucket_obj.objects.all():
        print(f'  {obj.key}')



