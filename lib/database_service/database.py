from lib.database_service.defaultmodel import DefaultChunkModel
from lib.database_service.getters import BlockFrameDatabaseGetters
from lib.database_service.initalisation import *


class BlockFrameDatabase(BlockFrameDatabaseGetters, BlockFrameDatabaseInit):
    def __init__(self, *args, **kwargs):
        self.class_model = (
            DefaultChunkModel
            if kwargs.get("class_model") is not None
            else kwargs.get("class_model")
        )
        self.database_obj = self.get_db()
        super().__init__(
            class_model=self.class_model,
            database_obj=self.database_obj,
        )
