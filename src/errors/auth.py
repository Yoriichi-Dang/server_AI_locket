from fastapi import HTTPException, status

class AccountAlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "Account already exists"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
class AccountNotFoundException(HTTPException):
    def __init__(self, detail: str = "Account not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)