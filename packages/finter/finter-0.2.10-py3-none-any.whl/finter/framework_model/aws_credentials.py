from finter.settings import get_api_client, logger
from finter.rest import ApiException
import finter

import pandas as pd
import s3fs


def get_aws_credentials(identity_name):
    api_instance = finter.AWSCredentialsApi(get_api_client())

    try:
        api_response = api_instance.aws_credentials_retrieve(identity_name=identity_name)
        return api_response
    except ApiException as e:
        print("Exception when calling AWSCredentialsApi->aws_credentials_retrieve: %s\n" % e)


def get_parquet_df(identity_name):

    credentials = get_aws_credentials(identity_name)
    fs = s3fs.S3FileSystem(
        key=credentials.aws_access_key_id,
        secret=credentials.aws_secret_access_key,
        token=credentials.aws_session_token,
    )

    s3_bucket_name = "finter-parquet"
    file_name = f"{identity_name}.parquet"
    s3_uri = f"s3://{s3_bucket_name}/{file_name}"

    with fs.open(s3_uri, "rb") as f:
        df = pd.read_parquet(f, engine="pyarrow")

    logger.info(f"Loading model by reading parquet: {identity_name}")
    return df
