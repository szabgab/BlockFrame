from BlockFrame import block_frame
import pathlib
from BlockFrame.database_service.defaultmodel import DefaultChunkModel

config_path = pathlib.Path("./config.json").absolute()
block_frame = block_frame.BlockFrame(config_path)

_chunker = block_frame.chunker
_chunker_db = block_frame.database
_chunker_db.create_table(DefaultChunkModel)

data = _chunker_db.get_all()

_chunker.target(file_name="random.txt", size=5)
# _chunker.generic_chunking()
