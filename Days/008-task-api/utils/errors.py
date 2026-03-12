from fastapi import HTTPException, status
from datetime import datetime


class APIError(HTTPException):

    def __init__(self, status_code, code, message, details=None):

        super().__init__(
            status_code=status_code,
            detail={
                "error": {
                    "code": code,
                    "message": message,
                    "details": details,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )


class TaskNotFoundError(APIError):

    def __init__(self, task_id):

        super().__init__(
            status.HTTP_404_NOT_FOUND,
            "TASK_NOT_FOUND",
            "Task not found",
            f"Task with ID {task_id} does not exist"
        )


class TagNotFoundError(APIError):

    def __init__(self, tag_id):

        super().__init__(
            status.HTTP_404_NOT_FOUND,
            "TAG_NOT_FOUND",
            "Tag not found",
            f"Tag with ID {tag_id} does not exist"
        )


class AuthenticationError(APIError):

    def __init__(self):

        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "AUTHENTICATION_FAILED",
            "Invalid credentials",
            "Email or password incorrect"
        )