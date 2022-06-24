import requests

print(
    requests.post(
        'https://word-sim-s3l3zbt4qq-ue.a.run.app:8080/predictions',
        # 'http://0.0.0.0:8080/predictions',
        json=dict(
            api_key='FD0568E53F09CD0B8050B492B142F35A94DB7F4E241A217ACCC1B2B2A4FDB63B',
            source="Hola",
            target="Hello",
        )
    ).content
)