from rest_framework.response import Response
from typing import Optional,Any


class ApiResponse(Response):
    def __init__(
        self,
        msg: str,
        data: Optional[Any] = None,
        errors: Optional[Any] = None,
        status: int = 200,
    ):
        resp = { 
            "errorFlag": "true" if status != 200 else "false", 
            "statusCode": "99" if status != 200 else "00",
            # "status": status in range(200, 300),
            "statusMsg": msg,
            "data": data,
            "errors": errors,
        }
        super().__init__(data=resp, status=status)

class SuccessApiResponse(ApiResponse):
    def __init__(self, msg, data):
        super(SuccessApiResponse, self).__init__(msg, data)


class FailureApiResponse(ApiResponse):
    def __init__(self, msg, errors=None):
        super(FailureApiResponse, self).__init__(msg, errors=errors, status=400)


class ServerErrorApiResponse(ApiResponse):
    def __init__(self):
        super(ServerErrorApiResponse, self).__init__("Server error", status=500)
