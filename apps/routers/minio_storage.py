import minio
from minio import Minio

minioClient = Minio('127.0.0.1:9000',
                    access_key='QuQZkQn2KfWJiuDIBsbO',
                    secret_key='2zNnTe2SIgjwuudMPMHjyDo8QeFiHHHb0nYGysWb',
                    secure=False)

BUCKET_NAME = "arava"
if not minioClient.bucket_exists(BUCKET_NAME):
    minioClient.make_bucket(BUCKET_NAME)
