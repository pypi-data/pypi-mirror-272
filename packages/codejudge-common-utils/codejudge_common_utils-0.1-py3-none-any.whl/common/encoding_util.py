import base64


class EncodeDecode:

    @classmethod
    def encode_credentials(cls, credentials):
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return encoded_credentials
