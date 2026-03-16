from fastapi import HTTPException

def ApiError(message):
    raise HTTPException(status_code=400, detail=message)