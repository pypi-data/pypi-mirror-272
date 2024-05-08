import hashlib
import base64
import base58
import jwt


class EncodeUtils:
    def __init__(self, password=None) -> None:
        self.password = password

    @staticmethod
    def hexIntEncode(data: int):
        return hex(data)

    @staticmethod
    def hexIntDecode(data: str):
        return int(data, base=16)

    @staticmethod
    def hexStringEncode(data: str, encoding="utf-8"):
        return data.encode(encoding).hex()

    @staticmethod
    def hexStringDecode(data: str, encoding="utf-8"):
        return bytes.fromhex(data).decode(encoding)

    @staticmethod
    def base58Encode(data: str, encoding="utf-8"):
        return base58.b58encode(data.encode(encoding)).decode(encoding)

    @staticmethod
    def base58Decode(data: str, encoding="utf-8"):
        return base58.b58decode(data).decode(encoding)

    @staticmethod
    def generateHash256(msg, salt="", encodeMethod="ascii"):
        hash256 = hashlib.sha256((msg[-2:] + salt).encode(encodeMethod))
        hash256.update(msg.encode(encodeMethod))
        return hash256.hexdigest(), hash256.digest()

    @staticmethod
    def verifyHash256(msg, hashMsg, salt=""):
        if EncodeUtils.generateHash256(msg, salt=salt) == hashMsg:
            return True
        else:
            return False

    @staticmethod
    def generateMD5(msg, salt="", encodeMethod="ascii"):
        md5 = hashlib.md5((msg[-2:] + salt).encode(encodeMethod))
        md5.update(msg.encode(encodeMethod))
        return md5.hexdigest(), md5.digest()

    @staticmethod
    def verifyMD5(msg, hashMsg, salt=""):
        if EncodeUtils.generateMD5(msg, salt=salt) == hashMsg:
            return True
        else:
            return False

    @staticmethod
    def generateExpireCode(expire: int | None = None):
        from datetime import datetime

        timenow = int(datetime.now().timestamp)

    def jwtEncode(self, data: dict):
        return jwt.encode(data, key=self.password)

    def jwtDecode(self, data: str):
        return jwt.decode(data, key=self.password, algorithms="HS256")

    def encrypt_message(self, key: bytes(16), data: bytes):
        from Crypto.Cipher import AES

        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext, tag, nonce

    def encryptMessageWithPassword(self, data: str):
        if not self.password:
            raise (TypeError("password must provide as str"))
        key = EncodeUtils.generateMD5(self.password)[1]
        data = data.encode()
        cipherData = self.encrypt_message(key, data)
        cipherDataStr = (
            cipherData[0].hex() + "." + cipherData[1].hex() + "." + cipherData[2].hex()
        )
        return cipherDataStr

    def decrypt_message(self, key, ciphertext, tag, nonce):
        from Crypto.Cipher import AES

        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data

    def decryptMessageWithPassword(self, cipherDataStr: str):
        if not self.password:
            raise (TypeError("password must provide as str"))
        cipherDataStrs = cipherDataStr.split(".")
        key = EncodeUtils.generateMD5(self.password)[1]
        data = self.decrypt_message(
            key,
            bytes.fromhex(cipherDataStrs[0]),
            bytes.fromhex(cipherDataStrs[1]),
            bytes.fromhex(cipherDataStrs[2]),
        )
        return data.decode()
