from typing import Optional

import boto3
from botocore.client import BaseClient


class Client:
    """
    wrapper for AWS client
    """
    def __init__(
            self,
            service_name: str,
            region_name: str,
            aws_access_key_id: str = None,
            aws_secret_access_key: str = None
    ):
        self.service_name = service_name
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self._client: Optional[BaseClient] = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def _create_client(self) -> BaseClient:
        return boto3.session.Session().client(
            service_name=self.service_name,
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

    def connect(self):
        self._client = self._create_client()

    def disconnect(self):
        self._client.close()
        del self._client
