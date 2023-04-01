File Chunker
CCIF = chunk construction information
```python
if __name__ == "__main__":
  

    chunker = Chunker("<your file name>", 5)
    chunker.run()

    for file in scan_for_ccif_files():
        reconstruct_controller = Reconstruct(file)
        reconstruct_controller.run()
```
