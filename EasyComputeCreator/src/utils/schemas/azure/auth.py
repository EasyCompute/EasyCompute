from pydantic import BaseModel


class AzureAccessKey(BaseModel):
    subscription_id: str
    client_id: str
    secret: str
    tenant: str
