from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated, PermissionDenied

def api_exception_handler(exception, context):
    """
    Wraps all DRF exceptions into a consistent response format:
    { 
        "ok": false, 
        "error": { 
            "code": "<slug>", 
            "message": "...", 
            "field_errors": {...} 
        } 
    }
    """
    response = exception_handler(exception, context)

    # if DRF handled the exception, customize the response format
    if response is not None:
        code = "error"
        message = None
        field_errors = None

        if isinstance(exception, ValidationError):
            code = "validation_error"
            message = "Input field is not valid."
            field_errors = response.data
        elif isinstance(exception, (AuthenticationFailed, NotAuthenticated)):
            code = "auth_failed"
            message = "Authentication is required."
        elif isinstance(exception, PermissionDenied):
            code = "permission_denied"
            message = "Permission denied."
        else:
            # ohter exceptions like NotFound, MethodNotAllowed, etc.
            message = response.data if isinstance(response.data, str) else None

        data = {"ok": False, "error": {"code": code, "message": message}}
        if field_errors:
            data["error"]["field_errors"] = field_errors
        return Response(data, status=response.status_code)

    # if DRF did not handle the exception, return a generic 500 error response
    return Response(
        {"ok": False, "error": {"code": "server_error", "message": "서버 오류가 발생했습니다."}},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )