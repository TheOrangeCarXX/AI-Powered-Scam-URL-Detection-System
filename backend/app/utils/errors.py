from fastapi import HTTPException

def bad_request(message: str):
    raise HTTPException(
        status_code=400,
        detail={
            "success": False,
            "error_code": "BAD_REQUEST",
            "message": message
        }
    )

def server_error():
    raise HTTPException(
        status_code=500,
        detail={
            "success": False,
            "error_code": "SERVER_ERROR",
            "message": "Something went wrong"
        }
    )
