import json
import os
import subprocess
from urllib import request
import requests
import uuid

import pytest

auth_token = (
    subprocess.run(
        ["gcloud", "auth", "print-identity-token"],
        stdout=subprocess.PIPE,
        check=True,
    )
    .stdout.strip()
    .decode()
)

service_url = 'http://localhost:8080'
resp = requests.get(service_url)
print(resp.content)

resp = requests.post(
    f"{service_url}/predictions",
    # headers={"Authorization": f"Bearer {auth_token}"},
    json=dict(
        source="Hola",
        target="Hello",
    )
)
print(resp.content)

resp = requests.post(
    f"{service_url}/predictions",
    # headers={"Authorization": f"Bearer {auth_token}"},
    json=dict(
        source="Holaao",
        target="Hello",
    )
)
print(resp.content)
