"""Mozilla IndexedDB object database tools for Python."""
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Credits:
#   – Source was heavily inspired by
#     https://searchfox.org/mozilla-central/rev/cc2040bf219ca3279405e09428f9457d41616bf9/dom/indexedDB/Key.cpp
#   – Python source code by Alexander Schlarb, 2020.

import datetime
import enum
import math
import io
import os
import struct
import sqlite3
import time
import typing as ty

from pyWhatsUpp.utils import snappy
from . import mozserial


class KeyType(enum.IntEnum):
    TERMINATOR = 0
    FLOAT      = 0x10
    DATE       = 0x20
    STRING     = 0x30
    BINARY     = 0x40
    ARRAY      = 0x50

class KeyCodec:
    ONE_BYTE_LIMIT = 0x7E
    TWO_BYTE_LIMIT = 0x3FFF + 0x7F
    
    ONE_BYTE_ADJUST = 1
    TWO_BYTE_ADJUST = -0x7F
    THREE_BYTE_SHIFT = 6
    
    MAX_ARRAY_COLLAPSE = 3
    
    @classmethod
    def encode(cls, value: object) -> bytes:
        buf = bytearray()
        cls._encode(buf, value, set())
        
        # TrimBuffer
        while buf[-1] == int(KeyType.TERMINATOR):
            buf.pop()
        
        return bytes(buf)
    
    @classmethod
    def decode(cls, value: bytes) -> object:
        result, index = cls._decode(value)
        assert index >= len(value)
        return result
    
    @classmethod
    def _encode(cls, buf: bytearray, value: object, seen: ty.Set[int], type_off: int = 0):
        if id(value) in seen:
            raise ValueError("Cannot encode recursive datastructures")
        seen.add(id(value))
        
        if isinstance(value, (int, float)):
            if math.isnan(value):
                raise ValueError("Cannot encode NaN")
            
            buf += cls.encode_number(value, type_off)
            return
        
        if isinstance(value, str):
            buf += cls.encode_string(value, type_off)
            return
        
        if isinstance(value, time.struct_time):
            timestamp = time.mktime(value)
            timezone  = datetime.timezone(datetime.timedelta(seconds=value.tm_gmtoff))
            value = datetime.datetime.fromtimestamp(timestamp, timezone)
        
        if isinstance(value, datetime.datetime):
            value = value.astimezone(datetime.timezone.utc).timestamp()
            buf += cls._encode_number(value, int(KeyType.DATE) + type_off)
            return
        
        if isinstance(value, (bytes, bytearray, memoryview)):
            buf += cls.encode_binary(value, type_off)
            return
        
        if isinstance(value, (list, tuple)):
            cls._encode_list(buf, value, seen, type_off)
            return
        
        raise ValueError(f"Cannot encode {repr(value)}")
    
    @classmethod
    def _decode(cls, buf: bytes, index: int = 0, type_off: int = 0) -> object:
        type = buf[index] - type_off
        if type >= KeyType.ARRAY:
            result = []
            
            type_off += KeyType.ARRAY
            if type_off == KeyType.ARRAY * cls.MAX_ARRAY_COLLAPSE:
                index   += 1
                type_off = 0
            
            while index < len(buf) and buf[index] - type_off != KeyType.TERMINATOR:
                item, index = cls._decode(buf, index, type_off)
                result.append(item)
                
                type_off = 0
            
            assert index >= len(buf) or buf[index] - type_off == KeyType.TERMINATOR, \
                   "Should have found end-of-array marker"
            
            return tuple(result), index+1
        elif type == KeyType.STRING:
            return cls._decode_string(buf, index, KeyType.STRING, type_off)
        elif type == KeyType.DATE:
            timestamp, index = cls._decode_number(buf, index, KeyType.DATE)
            
            result = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
            return result, index
        elif (type == KeyType.FLOAT):
            return cls._decode_number(buf=buf, index=index, type=KeyType.FLOAT)
        elif type == KeyType.BINARY:
            return cls._decode_string(buf, index, KeyType.BINARY, type_off)
        else:
            raise ValueError(f"Unknown key type {type}")
    
    @classmethod
    def encode_number(cls, value: ty.Union[int, float], type_off: int = 0) -> bytes:
        buf = bytearray()
        cls._encode_number(buf, float(value), int(KeyType.FLOAT) + type_off)
        return bytes(buf)
    
    def _encode_number(cls, buf: bytearray, value: float, type: int) -> bytes:
        # Write type marker
        buf.append(type)
        
        as_int = struct.unpack("=q", struct.pack("=d", value))[0]
        if value < 0:
            as_int = (0 - as_int) & 0xFFFFFFFFFFFFFFFF
        else:
            as_int |= 0x7000000000000000
        
        buf.append(struct.pack(">q", as_int))
    
    @classmethod
    def _decode_number(cls, buf: bytes, index: int, type: int) -> float:
        assert buf[index] % int(KeyType.ARRAY) == type, "Don't call me!"
        index += 1
        
        value = struct.unpack(">q", buf[index:index+8].ljust(8, b"\0"))[0]
        if value & 0x8000000000000000:
            value &= 0x7FFFFFFFFFFFFFFF
        else:
            value = 0 - value
        index += 8
        
        return struct.unpack("=d", struct.pack("=q", value))[0], index
    
    @classmethod
    def encode_binary(cls, value: bytes, type_off: int = 0) -> bytes:
        buf = bytearray()
        cls._encode_string(buf, value.decode("latin-1"), int(KeyType.BINARY) + type_off)
        return bytes(buf)
    
    @classmethod
    def encode_string(cls, value: str, type_off: int = 0) -> bytes:
        buf = bytearray()
        cls._encode_string(buf, value, int(KeyType.STRING) + type_off)
        return bytes(buf)
    
    @classmethod
    def _encode_string(cls, buf: bytearray, value: str, type: int):
        # Write type marker
        buf.append(type)
        
        # Encode string
        for uscalar in map(ord, value):
            # Strings are encoded per UTF-16 codepoint
            if uscalar <= 0xFFFF:
                codepoints = (uscalar,)
            else:
                codepoints = ((uscalar >> 10) | 0xD800, (uscalar & 0x3FF) | 0xDC00)
            
            for c in codepoints:
                if c <= cls.ONE_BYTE_LIMIT:
                    buf.append(c + cls.ONE_BYTE_ADJUST)
                elif c <= cls.TWO_BYTE_LIMIT:
                    c += cls.TWO_BYTE_ADJUST + 0x8000
                    buf.append((c >> 8) & 0xFF)
                    buf.append((c >> 0) & 0xFF)
                else:
                    c = (c << cls.THREE_BYTE_SHIFT) | 0x00C00000
                    buf.append((c >> 16) & 0xFF)
                    buf.append((c >> 8)  & 0xFF)
                    buf.append((c >> 0)  & 0xFF)
        
        buf.append(int(KeyType.TERMINATOR))
    
    @classmethod
    def _decode_string(cls, buf: bytes, index: int, type: int, type_off: int) -> ty.Union[str, bytes]:
        assert buf[index] % int(KeyType.ARRAY) == type, "Don't call me!"
        index += 1
        
        result = bytearray()
        while index < len(buf) and buf[index] - type_off != KeyType.TERMINATOR:
            c = buf[index]
            index += 1
            
            if c & 0x80 == 0:
                c -= cls.ONE_BYTE_ADJUST
            elif c & 0x40 == 0:
                c = c << 8
                if index < len(buf):
                    c |= buf[index]
                    index += 1
                c -= cls.TWO_BYTE_ADJUST - 0x8000
            elif type != KeyType.BINARY:
                c = c << (16 - cls.THREE_BYTE_SHIFT)
                if index < len(buf):
                    c |= buf[index] << (8 - cls.THREE_BYTE_SHIFT)
                    index += 1
                if index < len(buf):
                    c |= buf[index] >> cls.THREE_BYTE_SHIFT
                    index += 1
            
            if type != KeyType.BINARY:
                result += c.to_bytes(4, "little")
            else:
                result.append(c & 0xFF)
        
        if type != KeyType.BINARY:
            result = result.decode("UTF-32le")
        return result, index
    
    @classmethod
    def _encode_list(cls, buf: bytearray, value: list, seen: ty.Set[int], type_off: int = 0):
        # Key::ArrayValueEncoder::BeginSubkeyList
        type_off += int(KeyType.ARRAY)
        if type_off == int(KeyType.ARRAY) * cls.MAX_ARRAY_COLLAPSE:
            buf.append(type_off)
            type_off = 0
        assert type_off % int(KeyType.ARRAY) == 0, \
               "Current type offset must indicate beginning of array"
        assert type_off < int(KeyType.ARRAY) * cls.MAX_ARRAY_COLLAPSE
        
        for entry in value:
            # Key::ArrayValueEncoder::ConvertSubkey
            cls._encode(buf, entry, seen, type_off)
            type_off = 0
        
        # Key::ArrayValueEncoder::EndSubkeyList
        buf.append(int(KeyType.TERMINATOR) + type_off)


class IndexedDB(sqlite3.Connection):
    def __init__(self, dbpath: ty.Union[os.PathLike, str, bytes]):
        super().__init__(dbpath)
    
    def read_object(self, key_name: object) -> object:
        key = KeyCodec.encode(key_name)
        
        # Query data
        cur = self.cursor()
        cur.execute("SELECT data, file_ids FROM object_data WHERE key=?", (key,))
        result = cur.fetchone()
        if result is None:
            raise KeyError(key_name)
        
        # Validate data
        data, file_ids = result
        assert file_ids is None  #XXX: TODO
        
        # Parse data
        with io.BytesIO(data) as buff:
            decompressed = snappy.decompress(buff)
        
        reader = mozserial.Reader(io.BufferedReader(io.BytesIO(decompressed)))
        return reader.read()
    
    def read_objects(self) -> ty.Dict[object, object]:
        items = {}
        
        # Query data
        cur = self.cursor()
        cur.execute("SELECT key, data, file_ids FROM object_data")
        result = cur.fetchone()
        while result is not None:
            # Validate data
            key_name, data, file_ids = result
            assert file_ids is None  #XXX: TODO
            
            # Parse data
            with io.BytesIO(data) as buff:
                decompressed = snappy.decompress(buff)
            
            reader = mozserial.Reader(io.BufferedReader(io.BytesIO(decompressed)))
            content = reader.read()
            
            items[KeyCodec.decode(key_name)] = content
            
            result = cur.fetchone()
        
        return items
    
    def list_objects(self) -> ty.List[object]:
        key_names = []
        
        # Query data
        cur = self.cursor()
        cur.execute("SELECT key FROM object_data")
        result = cur.fetchone()
        while result is not None:
            key_names.append(KeyCodec.decode(result[0]))
            result = cur.fetchone()
        
        return key_names
    
    def count_objects(self) -> ty.List[object]:
        # Query data
        cur = self.cursor()
        cur.execute("SELECT COUNT(*) FROM object_data")
        result = cur.fetchone()
        assert result is not None
        
        return result[0]
