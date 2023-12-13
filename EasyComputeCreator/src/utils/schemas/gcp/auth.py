from pydantic import BaseModel


class GCPAccessKey(BaseModel):
    project_id: str
    credentials: str