import boto3

# Connect to AWS Systems Manager
ssm = boto3.client("ssm", region_name="ap-south-1")

# Parameter details
# parameter_name = "/myapp/database/username"
# parameter_value = "admin123"

# # Create parameter
# response = ssm.put_parameter(
#     Name=parameter_name,
#     Value=parameter_value,
#     Type="String",
#     Overwrite=True
# )

# print("Parameter created successfully!")
# print("Parameter Name:", parameter_name)

# Retrieve parameter
response = ssm.get_parameter(
    Name="/myapp/database/username"
)

value = response["Parameter"]["Value"]

print("Retrieved Value:", value)