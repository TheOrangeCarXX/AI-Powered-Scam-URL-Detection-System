from fastapi import HTTPException

# Utility function for 400 Bad Request error
def bad_request(message: str):
    raise HTTPException(
        status_code=400,
        detail={
            "success": False,
            "error_code": "BAD_REQUEST",
            "message": message
        }
    )

# Utility function for 404 Not Found error
def server_error():
    raise HTTPException(
        status_code=500,
        detail={
            "success": False,
            "error_code": "SERVER_ERROR",
            "message": "Something went wrong"
        }
    )
