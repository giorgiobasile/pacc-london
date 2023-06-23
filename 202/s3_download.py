from prefect_aws.s3 import S3Bucket
from prefect import flow
from botocore.client import Config
from botocore import UNSIGNED


@flow
def sentinel_2_download():
    s3_block = S3Bucket.load("aws-sentinel-2-cogs")

    s3_block.download_object_to_path(from_path="sentinel-s2-l2a-cogs/31/U/GR/2023/3/S2A_31UGR_20230303_0_L2A/B04.tif", to_path="./sample.tiff")


if __name__ == "__main__":
    sentinel_2_download()