from BlockFrame import block_frame
import pathlib

config_path = pathlib.Path("./config.json").absolute()
block_frame = block_frame.BlockFrame(config_path)
_chunker = block_frame.chunker
_chunker.target(file_name="random.txt", size=5)
_chunker.generic_chunking()
