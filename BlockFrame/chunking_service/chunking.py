import hashlib
import os
import uuid
import pathlib
from ..database_service.defaultmodel import DefaultChunkModel, ChunkHashes


class ChunkHandler:
    def __init__(self, *args, **kwargs) -> None:
        self.config = kwargs.get("config")
        self.path = self.config["file-storage-path"]
        self.db = kwargs.get("db")

    def target(self, file_name, size, files: list = None):
        self.file_name = file_name
        self.size = size
        self.primary_uuid = uuid.uuid4()
        self.original_file_hash = ""
        self.chunk_file_hashes = []
        self.chunk_file_uid = []
        return "correctly targetted"

    def __dir(self):
        try:
            return (
                pathlib.Path(self.config.get("file-storage-path"))
                if pathlib.Path(self.config.get("file-storage-path"))
                is pathlib.Path(self.config.get("file-storage-path")).exists
                else pathlib.Path(self.config.get("file-storage-path")).mkdir()
            )
        except FileExistsError:
            return pathlib.Path(self.config.get("file-storage-path"))

    def chunks(self):
        _size = os.stat(self.file_name).st_size // self.size
        with open(self.file_name, "rb") as f:
            while content := f.read(_size):
                yield content

    def produce_chunks(self):
        split_files = self.chunks()
        count = 0
        for chunk in split_files:
            _hash = hashlib.sha256()
            _file_chunk_uid = uuid.uuid4()

            with open(
                f"{pathlib.Path(self.path).absolute()}/{self.primary_uuid}_chunk_{_file_chunk_uid}_{count}.chunk",
                "wb+",
            ) as f:
                _hash.update(f.read())
                count += 1
                f.write(bytes(chunk))
            self.chunk_file_uid.append(_file_chunk_uid)
            self.chunk_file_hashes.append(_hash.hexdigest())

    def hasher(self):
        _hash = hashlib.sha256()
        with open(self.file_name, "rb") as file:
            chunk = 0
            while chunk != b"":
                chunk = file.read(1024)
                _hash.update(chunk)
        self.original_file_hash = _hash.hexdigest()

    def save_to_db(self):
        with self.db as session:
            model = DefaultChunkModel(
                file_uuid=str(self.primary_uuid),
                file_name=self.file_name,
                size=self.size,
                original_file_hash=self.original_file_hash,
                split_length=len(self.chunk_file_uid),
                linking_id=str(self.primary_uuid),
            )
            for _hash, _uid in zip(self.chunk_file_hashes, self.chunk_file_uid):
                model.hashes.append(
                    ChunkHashes(
                        chunk_hash=_hash,
                        linking_id=str(self.primary_uuid),
                        chunk_length=len(_hash),
                        chunk_size=len(str(_uid)),
                    )
                )
            session.add(model)
            session.commit()

    def generic_chunking(self):
        self.produce_chunks()
        self.hasher()
        self.save_to_db()
