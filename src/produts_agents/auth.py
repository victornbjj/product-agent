from fastapi import Header, HTTPException
from http import HTTPStatus



def get_current_user(x_user_id: str | None = Header(default=None)) -> str:

    user_id = (x_user_id or "").strip()

    if not user_id or len(user_id) > 50:
          raise HTTPException(
               status_code=HTTPStatus.UNAUTHORIZED,
               detail="Header X-User-Id ausente ou inválido."
          ) 
     
    return user_id