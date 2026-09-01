from fastapi import Header, HTTPException, status
from src.config import settings

async def verify_admin(admin_token: str = Header(...)):
    if admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You are not an administrator.."
        )
    return True
