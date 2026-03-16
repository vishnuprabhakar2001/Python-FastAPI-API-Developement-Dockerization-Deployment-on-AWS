from fastapi import UploadFile, File
from src.models.user_model import get_user_collection
from src.utils.api_error import ApiError
from src.utils.api_response import ApiResponse
from src.config.cloudinary_config import cloudinary
from jose import jwt
import os
from bson import ObjectId

JWT_SECRET = os.getenv("JWT_SECRET")


# -------------------------------
# Registration
# -------------------------------
async def register_user(data):

    user_collection = get_user_collection()

    if user_collection.find_one({"email": data.email}):
        ApiError("This user is already registered")

    user = {
        "f_name": data.f_name,
        "l_name": data.l_name,
        "email": data.email,
        "phone": data.phone,
        "address": data.address
    }

    result = user_collection.insert_one(user)

    token = jwt.encode(
        {"id": str(result.inserted_id)},
        JWT_SECRET,
        algorithm="HS256"
    )

    user["_id"] = str(result.inserted_id)
    return ApiResponse(
        "User registered successfully",
        {
            "user": user,
            "token": token
        }
    )


# -------------------------------
# Get All Profiles
# -------------------------------
async def get_profile():

    user_collection = get_user_collection()

    users = list(user_collection.find())

    if not users:
        ApiError("No users found")

    for user in users:
        user["_id"] = str(user["_id"])

    return ApiResponse(
        "All profiles fetched successfully",
        users
    )


# -------------------------------
# Update Profile
# -------------------------------
async def update_profile(
    userId,
    token,
    f_name,
    l_name,
    email,
    phone,
    address,
    file: UploadFile | None
):

    user_collection = get_user_collection()

    decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

    if decoded["id"] != userId:
        ApiError("Unauthorized request")

    update_data = {}

    if f_name:
        update_data["f_name"] = f_name
    if l_name:
        update_data["l_name"] = l_name
    if email:
        update_data["email"] = email
    if phone:
        update_data["phone"] = phone
    if address:
        update_data["address"] = address

    # upload image if provided
    if file:
        upload_result = cloudinary.uploader.upload(file.file)
        update_data["profileImage"] = upload_result["secure_url"]

    user_collection.update_one(
        {"_id": ObjectId(userId)},
        {"$set": update_data}
    )

    return ApiResponse(
        "Profile updated successfully",
        update_data
    )


# -------------------------------
# Get Profile By ID
# -------------------------------
async def get_profile_by_id(userId):

    user_collection = get_user_collection()

    user = user_collection.find_one({"_id": ObjectId(userId)})

    if not user:
        ApiError("User not found")

    user["_id"] = str(user["_id"])

    return ApiResponse(
        "User fetched successfully",
        user
    )


# -------------------------------
# Delete Profile By ID
# -------------------------------
async def delete_profile_by_id(userId):

    user_collection = get_user_collection()

    user = user_collection.find_one({"_id": ObjectId(userId)})

    if not user:
        ApiError("User not found")

    user_collection.delete_one({"_id": ObjectId(userId)})

    return ApiResponse(
        "User deleted successfully",
        {"deletedUserId": userId}
    )