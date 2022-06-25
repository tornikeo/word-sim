# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This sample creates a secure two-service application running on Cloud Run.
# This test builds and deploys the two secure services
# to test that they interact properly together.

import json
import os
import subprocess
from urllib import request
import requests
import uuid

import pytest

# Unique suffix to create distinct service names
SUFFIX = uuid.uuid4().hex[:10]
PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT",'news-languages')
IMAGE_NAME = f"gcr.io/{PROJECT}/helloworld-{SUFFIX}"


@pytest.fixture
def container_image():
    # Build container image for Cloud Run deployment
    subprocess.check_call(
        [
            "gcloud",
            "builds",
            "submit",
            "--tag",
            IMAGE_NAME,
            "--project",
            PROJECT,
            "--quiet",
        ]
    )

    yield IMAGE_NAME

    # Delete container image
    subprocess.check_call(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            IMAGE_NAME,
            "--quiet",
            "--project",
            PROJECT,
        ]
    )


@pytest.fixture
def deployed_service(container_image):
    # Deploy image to Cloud Run
    service_name = f"helloworld-{SUFFIX}"
    subprocess.check_call(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            "--image",
            container_image,
            "--project",
            PROJECT,
            "--region=us-central1",
            "--platform=managed",
            "--no-allow-unauthenticated",
            "--set-env-vars=NAME=Test",
        ]
    )

    yield service_name

    subprocess.check_call(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            service_name,
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
            "--async",
            "--project",
            PROJECT,
        ]
    )


@pytest.fixture
def service_url_auth_token(deployed_service):
    # Get Cloud Run service URL and auth token
    service_url = (
        subprocess.run(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                deployed_service,
                "--platform=managed",
                "--region=us-central1",
                "--format=value(status.url)",
                "--project",
                PROJECT,
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )
    auth_token = (
        subprocess.run(
            ["gcloud", "auth", "print-identity-token"],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.strip()
        .decode()
    )

    yield service_url, auth_token

    # no deletion needed

def test_end_to_end(service_url_auth_token):
    service_url, auth_token = service_url_auth_token

    req = request.Request(
        f"{service_url}/", headers={"Authorization": f"Bearer {auth_token}"}
    )
    response = request.urlopen(req)
    assert response.status == 200

    body = response.read()
    assert "Hello Test!" == body.decode()


if __name__ == "__main__":
    service_url = 'https://word-sim-s3l3zbt4qq-ue.a.run.app/'
    auth_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjJiMDllNzQ0ZDU4Yzk5NTVkNGYyNDBiNmE5MmY3YjM3ZmVhZDJmZjgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA0MDI2NjIyOTkzMjE4OTQ2MDY2IiwiZW1haWwiOiJ0b3JuaWtlb25vcHJpc2h2aWxpQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiQkkxcmFOb0VXVGJ6LW1hMEl2T090QSIsImlhdCI6MTY1NjE2NzE3MSwiZXhwIjoxNjU2MTcwNzcxfQ.i77weUi9D2akAXi9N-suuQmtysugAadhlaahr60vEV9QzLHvmU2SyGnepOJoc60dNLfLsQQxv3nxxBVuEAQR3ZZ019gqhShGtBR_k-WzXh09kR0og219cvu54_IojkTv9nex7zAwkRQOT2Qy1Ptt-_ddMYo_mBjhI95gF3xcWYoLoB6inCpfo-cBghngAV5biqQpKIG-j8-SPMRtSf2ApXiwXPJJxzeJFnYTbd1rZpvnNxCC5RrJSsUss7E8mkP7ioB27WqHVH-MJSmJYcTnrf_qbEpKCyUSMjfiS1iZ0stlJzZDAqWQQXN0XEEvjDr1w9v4gYDcpS2uDo_UEGo_yg"
    resp = requests.get(
        f"{service_url}",
        headers={"Authorization": f"Bearer {auth_token}"},
        # json=dict(
        #     source="Hola",
        #     target="Hello",
        # )
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

    # service_url = 'http://localhost:9090'
    # auth_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjJiMDllNzQ0ZDU4Yzk5NTVkNGYyNDBiNmE5MmY3YjM3ZmVhZDJmZjgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA0MDI2NjIyOTkzMjE4OTQ2MDY2IiwiZW1haWwiOiJ0b3JuaWtlb25vcHJpc2h2aWxpQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiM1pyUnR5LTN3Q2JJSzNsZkUyUExWdyIsImlhdCI6MTY1NjE2MjEwMCwiZXhwIjoxNjU2MTY1NzAwfQ.hFtsyMNCgknLRoo7ssM4t2vFJGbNqo6PX5lQQ91ABNGt8CCU546cLeuISvfDyDbW95cR3uzbeYEJ6VuncTgYi_glJ6xVosM2TGF-heFLQqQ2zp7eTj4ZNJvYYF21xX-_8SX_ZKvHBFyu1rArrfNeYUTUPYNH1j9gaVpDcS7FsByldXwRX0Zy06Qoh7Z76oRVgrN-NKDp7kEBY1tRvFidpTOxw1uCGmEmG-Afx1PouY1rGsK8bdjoDR3OlfG05asN4wx3LOf2t6gkbwzDl0pGIQsb0Av6O5LpIC7IY-5K8k_wO1wIaSawgTC76p1hecbgbQ70HbTxLm5gePu8LrGG_g"
    # resp = requests.post(
    #     f"{service_url}/predictions",
    #     # headers={"Authorization": f"Bearer {auth_token}"},
    #     json=dict(
    #         source="Hola",
    #         target="Hello",
    #     )
    # )
    # print(resp.content)

    # resp = requests.post(
    #     f"{service_url}/predictions",
    #     # headers={"Authorization": f"Bearer {auth_token}"},
    #     json=dict(
    #         source="Holaao",
    #         target="Hello",
    #     )
    # )
    # print(resp.content)