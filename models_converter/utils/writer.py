class Writer:
    def __init__(self, endian='big'):
        self.endian = endian
        self.buffer = b''

    def write(self, data):
        self.buffer += data

    def writeUInteger(self, integer, length=1):
        self.buffer += integer.to_bytes(length, self.endian, signed=False)

    def writeInteger(self, integer, length=1):
        self.buffer += integer.to_bytes(length, self.endian, signed=True)

    def writeUInt64(self, integer):
        self.writeUInteger(integer, 8)

    def writeInt64(self, integer):
        self.writeInteger(integer, 8)

    def writeFloat(self, floating):
        exponent = 0
        sign = 1

        if floating == 0:
            self.writeUInt32(0)
        else:
            if floating < 0:
                sign = -1
                floating = -floating

            if floating >= 2 ** -1022:
                value = floating

                while value < 1:
                    exponent -= 1
                    value *= 2
                while value >= 2:
                    exponent += 1
                    value /= 2

            mantissa = floating / 2 ** exponent

            exponent += 127

            as_integer_bin = '0'
            if sign == -1:
                as_integer_bin = '1'

            as_integer_bin += bin(exponent)[2:].zfill(8)

            mantissa_bin = ''
            for x in range(24):
                bit = '0'
                if mantissa >= 1 / 2 ** x:
                    mantissa -= 1 / 2 ** x
                    bit = '1'
                mantissa_bin += bit

            mantissa_bin = mantissa_bin[1:]

            as_integer_bin += mantissa_bin
            as_integer = int(as_integer_bin, 2)

            self.writeUInt32(as_integer)

    def writeUInt32(self, integer):
        self.writeUInteger(integer, 4)

    def writeInt32(self, integer):
        self.writeInteger(integer, 4)

    def writeNUInt16(self, integer):
        self.writeUInt16(round(integer * 65535))

    def writeUInt16(self, integer):
        self.writeUInteger(integer, 2)

    def writeNInt16(self, integer):
        self.writeInt16(round(integer * 32512))

    def writeInt16(self, integer):
        self.writeInteger(integer, 2)

    def writeUInt8(self, integer):
        self.writeUInteger(integer)

    def writeInt8(self, integer):
        self.writeInteger(integer)

    def writeBool(self, boolean: bool):
        if boolean:
            self.writeUInt8(1)
        else:
            self.writeUInt8(0)

    writeUInt = writeUInteger
    writeInt = writeInteger

    writeULong = writeUInt64
    writeLong = writeInt64

    writeNUShort = writeNUInt16
    writeNShort = writeNInt16

    writeUShort = writeUInt16
    writeShort = writeInt16

    writeUByte = writeUInt8
    writeByte = writeInt8

    def writeChar(self, string):
        for char in list(string):
            self.buffer += char.encode('utf-8')

    def writeString(self, string):
        encoded = string.encode('utf-8')
        self.writeUShort(len(encoded))
        self.buffer += encoded
