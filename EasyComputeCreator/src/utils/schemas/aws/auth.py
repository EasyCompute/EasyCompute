from pydantic import BaseModel


class AWSAccessKey(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str