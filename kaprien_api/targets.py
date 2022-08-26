import json
from typing import Any, Dict, List, Optional

from kaprien_api import repository_metadata, settings_repository
from kaprien_api.utils import BaseModel, get_task_id


class ResponseData(BaseModel):
    targets: List[str]
    task_id: str


class Response(BaseModel):
    data: Optional[ResponseData]
    message: Optional[str]

    class Config:
        data_example = {
            "data": {
                "targets": ["file1.tar.gz", "file2.tar.gz"],
                "task_id": "06ee6db3cbab4b26be505352c2f2e2c3",
            },
            "message": "Target(s) successfully submitted.",
        }
        schema_extra = {"example": data_example}


class PayloadTargetsHashes(BaseModel):
    blake2b_256: str

    class Config:
        fields = {"blake2b_256": "blake2b-256"}


class TargetsInfo(BaseModel):
    length: int
    hashes: PayloadTargetsHashes
    custom: Optional[Dict[str, Any]]


class Targets(BaseModel):
    info: TargetsInfo
    path: str


class Payload(BaseModel):
    targets: List[Targets]

    class Config:
        with open("tests/data_examples/targets/payload.json") as f:
            content = f.read()
        payload = json.loads(content)
        schema_extra = {"example": payload}


def post(payload):
    task_id = get_task_id()
    repository_metadata.apply_async(
        kwargs={
            "action": "add_targets",
            "settings": settings_repository.to_dict(),
            "payload": payload.dict(by_alias=True),
        },
        task_id=task_id,
        queue="metadata_repository",
        acks_late=True,
    )
    data = {
        "targets": [target.path for target in payload.targets],
        "task_id": task_id,
    }
    return Response(data=data, message="Target(s) successfully submitted.")
