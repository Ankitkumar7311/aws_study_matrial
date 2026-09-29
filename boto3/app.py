import boto3

s3 = boto3.resource('s3')


# 1. LIST ALL BUCKETS
# print("Existing Buckets:")

# for bucket in s3.buckets.all():
#     print(bucket.name)


# # 2. CREATE BUCKET
# bucket_name = "my-boto3-test-bucket-123456789"

# s3.create_bucket(
#     Bucket=bucket_name,
#     CreateBucketConfiguration={
#         'LocationConstraint': 'ap-south-1'
#     }
# )

# print("\nBucket created:", bucket_name)


# 3. UPLOAD FILE TO BUCKET
# file_name = "test.txt"

# s3.Bucket("my-boto3-test-bucket-123456789").upload_file(
#      "app.py",
#     "test.txt"
# )

# print("File uploaded successfully")


# # 4. DOWNLOAD FILE FROM BUCKET
# s3.Bucket(bucket_name).download_file(
#     "test.txt",
#     "downloaded_test.txt"
# )

# print("File downloaded successfully")


# # 5. DELETE FILE FROM BUCKET
# s3.Object(bucket_name, "test.txt").delete()

# print("File deleted successfully")


# 6. DELETE BUCKET note-first we have to delete file from bucket because we can delete only empty file bucket

s3.Bucket("my-boto3-test-bucket-123456789").delete()

print("Bucket deleted successfully")