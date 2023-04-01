from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


class DatabaseInterface:
    Base = declarative_base()
    db_engine = create_engine("sqlite:///blockframe_db.db")
    async_session = sessionmaker(db_engine, class_=sessionmaker, expire_on_commit=False)

    def custom_uri(uri: str):
        async_engine = create_engine(uri)


class BlockFrameDatabaseInit(DatabaseInterface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.class_model = kwargs.get("class_model")
        if self.class_model is not None:
            self.db_model = self.class_model
        else:
            from defaultmodel import DefaultChunkModel
            self.db_model = DefaultChunkModel()
        self.initalise()

    def initalise(self):
        for db in self.get_db():
            self.create_table(self.db_model)
            with db.begin():
                self.create_table(self.db_model)
                db.commit()

    def create_table(self, db_model):
        with self.async_engine.begin() as conn:
            conn.run_sync(db_model.metadata.create_all)

    def get_db(self):
        session = self.async_session()
        try:
            return session
        finally:
            session.close_all()


class BlockFrameModelInstance(DatabaseInterface):
    def __new__(cls):
        instance = super().__new__(cls)
        return instance.Base


if __name__ == "__main__":
    cdb = BlockFrameModelInstance()


    class CustomBlockFrameModel(cdb):
        __tablename__ = "BlockFrame_model"
        id = Column(Integer(), primary_key=True)
        data = Column(String())


    chunk_db = BlockFrameDatabaseInit(CustomBlockFrameModel)
