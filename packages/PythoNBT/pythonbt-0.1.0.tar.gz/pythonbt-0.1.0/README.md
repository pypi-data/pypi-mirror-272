## PythoNBT

PythoNBT is a simple Named Binary Tag (NBT) library for Python capable of reading in both little and big endian formats that are compressed or uncompressed.

### Installation

```
pip install PythoNBT
```

### Usage

Reading java nbt files:

```python
from nbt import NBTReader

with open("myfile.dat", "rb") as f:
    NBTReader.read(f)
```

Reading bedrock nbt files:

```python
from nbt import NBTReader

with open("myfile.dat", "rb") as f:
    NBTReader.read(f, little_endian=True, compressor=None)
```

Reading bedrock level file (slight variation on regular bedrock nbt files):

```python
from nbt import BedrockLevel

with open("level.dat", "rb") as f:
    BedrockLevel.read(f)
```
