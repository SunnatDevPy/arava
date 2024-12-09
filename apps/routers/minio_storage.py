import minio
from minio import Minio

minioClient = Minio('backend1.mussi.uz:9000',
                    access_key='QuQZkQn2KfWJiuDIBsbO',
                    secret_key='2zNnTe2SIgjwuudMPMHjyDo8QeFiHHHb0nYGysWb',
                    secure=False)

BUCKET_NAME = "arava"
if not minioClient.bucket_exists(BUCKET_NAME):
    minioClient.make_bucket(BUCKET_NAME)
