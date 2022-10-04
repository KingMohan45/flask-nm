from typing import Optional

from flask import make_response

def api_response(data ,message: Optional[str],  status: Optional[bool], status_code: Optional[bool]) -> make_response:
    """
    This function is used to return a response in a standard format
    """
    if status_code is None:
        status_code = 200 if status else 400
    response = {
        'status': "success" if status else "failed",
        'message': message,
        'data': data
    }
    return make_response(response, 200)