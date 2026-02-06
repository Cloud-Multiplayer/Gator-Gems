from fastapi import APIRouter, HTTPException, Path
from typing import Annotated

from pydantic import BaseModel

from app.database.connections import SessionDep
from app.models.users import User


router = APIRouter()


class CreateUser(BaseModel):
    firstName: str
    lastName: str


@router.post("/users/{email_address}", description="Create a new user")
def create_user(
    email_address: Annotated[str, Path(title="Email address of the user to create")],
    user: CreateUser,
    session: SessionDep,
):
    existing_user = session.get(User, email_address)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(
        email_address=email_address,
        first_name=user.firstName,
        last_name=user.lastName,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return {"message": f"User with email {db_user.email_address} created successfully."}


@router.delete("/users/{email_address}", description="Delete an existing user")
def delete_user(
    email_address: Annotated[str, Path(title="Email address of the user to delete")],
    session: SessionDep,
):
    existing_user = session.get(User, email_address)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(existing_user)
    session.commit()

    return {
        "message": f"User with email {existing_user.email_address} deleted successfully."
    }


@router.get(
    "/users/{email_address}",
    description="Get user details by email address",
    response_model=User,
)
def get_user(
    email_address: Annotated[str, Path(title="Email address of the user to retrieve")],
    session: SessionDep,
):
    user = session.get(User, email_address)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
