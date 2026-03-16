from fastapi import APIRouter, UploadFile, File, Form
from src.schemas.user_schema import RegisterUser
from src.schemas.user_schema import GetProfileRequest


from src.controllers.user_controller import (
    register_user,
    get_profile,
    update_profile,
    get_profile_by_id,
    delete_profile_by_id
)

router = APIRouter()


@router.post("/registration")
async def register(data: RegisterUser):
    return await register_user(data)



@router.get("/getprofile")
async def profile():
    return await get_profile()


@router.put("/profileupdate")
async def update(
    userId: str = Form(...),
    token: str = Form(...),
    f_name: str | None = Form(None),
    l_name: str | None = Form(None),
    email: str | None = Form(None),
    phone: str | None = Form(None),
    address: str | None = Form(None),
    file: UploadFile | None = File(None)
):
    return await update_profile(
        userId, token, f_name, l_name, email, phone, address, file
    )



# -------------------------------
# Get Profile By ID
# -------------------------------
@router.get("/getprofilebyid/{userId}")
async def get_profile_id(userId: str):
    return await get_profile_by_id(userId)


# -------------------------------
# Delete Profile By ID
# -------------------------------
@router.delete("/deleteprofilebyid/{userId}")
async def delete_profile_id(userId: str):
    return await delete_profile_by_id(userId)