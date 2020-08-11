def bytesToString(bs):
        return bytes.decode(bs,encoding='utf8')

print(bytesToString(b'\x76696f6c6173'))
