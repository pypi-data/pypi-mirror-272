import gzip
import io

import netstruct


class Tag:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}(name={repr(self.name)}, value={repr(self.value)})"

    def serialize(self, little_endian=False):
        endian = b"<" if little_endian else b">"
        return netstruct.pack(
            endian + b"bH$", self._ID, self.name.encode("utf-8")
        ) + self.serialize_payload(endian)


class TagByte(Tag):
    _ID = 1

    def serialize_payload(self, endian):
        return self.value


class TagShort(Tag):
    _ID = 2

    def serialize_payload(self, endian):
        return netstruct.pack(endian + b"h", self.value)


class TagInt(Tag):
    _ID = 3

    def serialize_payload(self, endian):
        return netstruct.pack(endian + b"i", self.value)


class TagLong(Tag):
    _ID = 4

    def serialize_payload(self, endian):
        return netstruct.pack(endian + b"q", self.value)


class TagFloat(Tag):
    _ID = 5

    def serialize_payload(self, endian):
        return netstruct.pack(endian + b"f", self.value)


class TagDouble(Tag):
    _ID = 6

    def serialize_payload(self, endian):
        return netstruct.pack(endian + b"d", self.value)


class TagByteArray(Tag):
    _ID = 7

    def serialize_payload(self, endian):
        return netstruct.pack(endian + b"i", len(self.value)) + self.value


class TagString(Tag):
    _ID = 8

    def serialize_payload(self, endian):
        return netstruct.pack(endian + b"H$", self.value.encode("utf-8"))


class TagList(Tag):
    _ID = 9

    def serialize_payload(self, endian):
        return netstruct.pack(
            endian + b"bi", self.value[0]._ID, len(self.value)
        ) + b"".join(tag.serialize_payload(endian) for tag in self.value)


class TagCompound(Tag):
    _ID = 10

    def serialize_payload(self, endian):
        little_endian = True if endian == b"<" else False
        return b"".join(tag.serialize(little_endian) for tag in self.value) + b"\x00"


class TagIntArray(Tag):
    _ID = 11

    def serialize_payload(self, endian):
        return netstruct.pack(endian + b"i", len(self.value)) + b"".join(
            netstruct.pack(endian + b"i", val) for val in self.value
        )


class TagLongArray(Tag):
    _ID = 12

    def serialize_payload(self, endian):
        return netstruct.pack(endian + b"i", len(self.value)) + b"".join(
            netstruct.pack(endian + b"q", val) for val in self.value
        )


class BedrockLevel:
    def __init__(self, version, data):
        self.version = version
        self.data = data

    @classmethod
    def read(cls, buffer):
        version, _ = netstruct.unpack(b"<ii", buffer.read(8))
        data = NBTReader.read(buffer, little_endian=True, compressor=None)[0]
        return cls(version, data)

    def serialize(self):
        bin_data = self.data.serialize(True)
        return netstruct.pack(b"<ii", self.version, len(bin_data)) + bin_data

    def save(self, filename):
        with open(filename, "wb+") as f:
            return f.write(self.serialize())


class NBTReader:
    @staticmethod
    def _read_string(buffer, endian):
        it = netstruct.iter_unpack(endian + b"H$", buffer.read(2))

        req = next(it)
        while isinstance(req, int):
            if buffer.peek(1) == b"":
                raise EOFError

            req = it.send(buffer.read(req))

        return req[0].decode("utf-8")

    @classmethod
    def _get_tag(cls, tag_id, buffer, endian):
        match tag_id:
            case 1:
                return TagByte, buffer.read(1)

            case 2:
                return TagShort, netstruct.unpack(endian + b"h", buffer.read(2))[0]

            case 3:
                return TagInt, netstruct.unpack(endian + b"i", buffer.read(4))[0]

            case 4:
                return TagLong, netstruct.unpack(endian + b"q", buffer.read(8))[0]

            case 5:
                return TagFloat, netstruct.unpack(endian + b"f", buffer.read(4))[0]

            case 6:
                return TagDouble, netstruct.unpack(endian + b"d", buffer.read(8))[0]

            case 7:
                it = netstruct.iter_unpack(endian + b"i$", buffer.read(4))

                req = next(it)
                while isinstance(req, int):
                    if buffer.peek(1) == b"":
                        raise EOFError

                    req = it.send(buffer.read(req))

                return TagByteArray, req[0]

            case 8:
                return TagString, cls._read_string(buffer, endian)

            case 9:
                tag_id, length = netstruct.unpack(endian + b"bi", buffer.read(5))
                values = []
                for value in range(length):
                    typ, val = cls._get_tag(tag_id, buffer, endian)
                    values.append(typ("", val))
                return TagList, values

            case 10:
                return TagCompound, cls._read_compound(buffer, endian)

            case 11:
                length = netstruct.unpack(endian + b"i", buffer.read(4))[0]
                return TagIntArray, [
                    cls._get_tag(3, buffer, endian)[1] for _ in range(length)
                ]

            case 12:
                length = netstruct.unpack(endian + b"i", buffer.read(4))[0]
                return TagLongArray, [
                    cls._get_tag(4, buffer, endian)[1] for _ in range(length)
                ]

    @classmethod
    def _read_compound(cls, buffer, endian):
        tags = []

        while True:
            if buffer.peek(1) == b"":
                raise EOFError

            tag_id = buffer.read(1)[0]
            if tag_id == 0:
                return tags

            else:
                name = cls._read_string(buffer, endian)
                typ, val = cls._get_tag(tag_id, buffer, endian)
                tags.append(typ(name, val))

    @classmethod
    def read(cls, buffer, little_endian=False, compressor=gzip):
        endian = b"<" if little_endian else b">"

        if compressor is not None:
            buffer = io.BufferedReader(io.BytesIO(compressor.decompress(buffer.read())))

        output = []
        while buffer.peek(1) != b"":
            tag_id = buffer.read(1)[0]

            name = cls._read_string(buffer, endian)
            typ, val = cls._get_tag(tag_id, buffer, endian)
            output.append(typ(name, val))

        return output
