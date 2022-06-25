import json
import os
import subprocess
from urllib import request
import requests
import uuid

import pytest

service_url = 'https://word-sim-s3l3zbt4qq-ue.a.run.app/'


auth_token = (
    subprocess.run(
        ["gcloud", "auth", "print-identity-token"],
        stdout=subprocess.PIPE,
        check=True,
    )
    .stdout.strip()
    .decode()
)


resp = requests.get(
    f"{service_url}",
    headers={"Authorization": f"Bearer {auth_token}"},
)
print(resp.content)

resp = requests.post(
    f"{service_url}/predictions",
    headers={"Authorization": f"Bearer {auth_token}"},
    json=dict(
        source="Hola",
        target="Hello",
    )
)
print(resp.content)