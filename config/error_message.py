from ninja import Schema


class Http4xxMessage(Schema):
    code: str
    message: str
