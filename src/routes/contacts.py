from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query, Path

from src.database.connect_db import AsyncDBSession, get_session
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=1000),
    first_name: str = Query(default=None),
    last_name: str = Query(default=None),
    email: str = Query(default=None),
    session: AsyncDBSession = Depends(get_session),
):
    return await repository_contacts.read_contacts(
        offset, limit, first_name, last_name, email, session
    )


@router.get("/birthdays-in-{n}-days", response_model=List[ContactResponse])
async def read_contacts_with_birthdays_in_n_days(
    n: int = Path(ge=1, le=62),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=1000),
    session: AsyncDBSession = Depends(get_session),
):
    return await repository_contacts.read_contacts_with_birthdays_in_n_days(
        n, offset, limit, session
    )


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, session: AsyncDBSession = Depends(get_session)):
    contact = await repository_contacts.read_contact(contact_id, session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(
    body: ContactModel, session: AsyncDBSession = Depends(get_session)
):
    return await repository_contacts.create_contact(body, session)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, body: ContactModel, session: AsyncDBSession = Depends(get_session)
):
    contact = await repository_contacts.update_contact(contact_id, body, session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(
    contact_id: int, session: AsyncDBSession = Depends(get_session)
):
    contact = await repository_contacts.delete_contact(contact_id, session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The contact not found"
        )
    return contact