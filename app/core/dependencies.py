from typing import Annotated

from fastapi import Header, HTTPException, Depends


async def get_token_header(x_token: Annotated[str | None, Header()] = None):
    if x_token is None:
        return False
    
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    
    return True



# dependencies = [Depends(get_token_header)]
dependencies = []


