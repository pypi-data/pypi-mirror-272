import pathlib
import os

from typing import Optional

from aim._sdk.base.record import Record
from aim._core.storage.artifacts import registry


@Record.alias('aim.artifact')
class Artifact(Record):
    AIM_NAME = 'aim.Artifact'

    def __init__(self, path: str, *, uri: str, name: Optional[str] = None, **metadata):
        self._uri = uri

        path = pathlib.Path(path)
        if name is None:
            name = path.name

        self.storage['name'] = name
        self.storage['path'] = path.as_posix()
        self.storage['base_uri'] = uri
        self.storage['uri'] = os.path.join(uri, name)
        for key, val in metadata.items():
            self.storage[key] = val

    @property
    def name(self) -> str:
        return self.storage['name']

    @property
    def path(self):
        return self.storage['path']

    @property
    def uri(self):
        return self.storage['uri']

    def upload(self, block: bool = False):
        artifacts_uri = self.storage['base_uri']
        storage = registry.get_storage(artifacts_uri)
        storage.upload_artifact(self.path, artifact_path=self.name, block=block)

    def download(self, dest_dir: str) -> str:
        artifacts_uri = self.storage['base_uri']
        storage = registry.get_storage(artifacts_uri)
        return storage.download_artifact(self.name, dest_dir=dest_dir)
