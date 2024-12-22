import boto3

# Initialize ECS client
ecs_client = boto3.client('ecs', 'ap-south-1')

# Create a new ECS cluster
cluster_name = 'sdk-cluster'
response = ecs_client.create_cluster(
    clusterName=cluster_name,
    capacityProviders=['FARGATE']
)

print(f'Cluster {cluster_name} created successfully')

# Output the cluster ARN
cluster_arn = response['cluster']['clusterArn']
print(f'Cluster ARN: {cluster_arn}')

print("Creating a new task definition...")
task_definition = ecs_client.register_task_definition(
    family='weatherapp-task',
    containerDefinitions=[
        {
            'name': 'weatherapp-container',
            'image': 'uzair102/u_repo:weather_app-v1.8', # pulling from docker hub Private registry
            'repositoryCredentials': { 
                'credentialsParameter': 'arn:aws:secretsmanager:ap-south-1:AWS_ACCOUNT_ID:secret:Docker-hub-credentials-mENosM'
            },
            'cpu': 256,
            'memory': 1024,
            'essential': True,
            'portMappings': [
                {
                    'containerPort': 3000,
                    'hostPort': 3000,
                    'protocol': 'tcp',
                    'appProtocol': 'http'
                }
            ]
        }
    ],
    taskRoleArn='arn:aws:iam::AWS_ACCOUNT_ID:role/ecsTaskExecutionRole',
    executionRoleArn='arn:aws:iam::AWS_ACCOUNT_ID:role/ecsTaskExecutionRole',
    ephemeralStorage={
        'sizeInGiB': 21
    },
    runtimePlatform={
        'cpuArchitecture': 'X86_64',
        'operatingSystemFamily': 'LINUX'
    },
    requiresCompatibilities=['FARGATE'], 
    networkMode='awsvpc', 
    cpu='256',  
    memory='1024'  
)


print(f'Task definition created successfully')
# Output the task definition ARN
task_def_arn = task_definition['taskDefinition']['taskDefinitionArn']
print(f'Task definition ARN: {task_def_arn}')

print("Creating a new service...")
# Create a new ECS service
service_name = 'weatherapp-service'
response = ecs_client.create_service(
    cluster=cluster_name,
    serviceName=service_name,
    taskDefinition='weatherapp-task',
    desiredCount=1,
    launchType='FARGATE',
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': [
                'subnet-021e4c85656747d98',
                'subnet-091f161d52ffc95ac',
                'subnet-0f589277124822a92'
            ],
            'securityGroups': [
                'sg-0f7d983d4dc5cd3e2'
            ],
            'assignPublicIp': 'ENABLED'
        }
    },
    availabilityZoneRebalancing='ENABLED',
    healthCheckGracePeriodSeconds=123123123  
)

print(f'Service {service_name} created successfully')
# Output the service ARN
service_arn = response['service']['serviceArn']
print(f'Service ARN: {service_arn}')
