from collections import defaultdict
from datetime import datetime
from typing import List

from sqlalchemy import select

from src.database.connect_db import AsyncDBSession
from src.database.models import Contact
from src.schemas import ContactModel
from src.utils.is_leap_year import is_leap_year


async def read_contacts(
    offset: int,
    limit: int,
    first_name: str,
    last_name: str,
    email: str,
    session: AsyncDBSession,
) -> List[Contact] | None:
    stmt = select(Contact)
    if first_name:
        stmt = stmt.filter(Contact.first_name.like(f"%{first_name}%"))
    if last_name:
        stmt = stmt.filter(Contact.last_name.like(f"%{last_name}%"))
    if email:
        stmt = stmt.filter(Contact.email.like(f"%{email}%"))
    stmt = stmt.offset(offset).limit(limit)
    contacts = await session.execute(stmt)
    return contacts.scalars()


async def read_contacts_with_birthdays_in_n_days(
    n: int,
    offset: int,
    limit: int,
    session: AsyncDBSession,
) -> List[Contact] | None:
    stmt = select(Contact)
    contacts = await session.execute(stmt)
    contacts = contacts.scalars()
    current_date = datetime.now().date()
    tmp = defaultdict(list)
    is_leap_year_flag = is_leap_year(current_date.year)
    for contact in contacts:
        date_of_birth = contact.birthday
        if (
            not is_leap_year_flag
            and date_of_birth.month == 2
            and date_of_birth.day == 29
        ):
            date_delta = (
                datetime(year=current_date.year, month=3, day=1).date() - current_date
            )
        else:
            date_delta = (
                datetime(
                    year=current_date.year,
                    month=date_of_birth.month,
                    day=date_of_birth.day,
                ).date()
                - current_date
            )
        delta_days = date_delta.days
        if delta_days < n - 365:
            delta_days += 365 + is_leap_year_flag
        if delta_days in range(n):
            tmp[delta_days].append(contact)

    result = []
    for delta_days in range(n):
        result = result + tmp[delta_days]

    return result[offset:limit]


async def read_contact(contact_id: int, session: AsyncDBSession) -> Contact | None:
    stmt = select(Contact).filter(Contact.id == contact_id)
    contact = await session.execute(stmt)
    return contact.scalar()


async def create_contact(body: ContactModel, session: AsyncDBSession) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        birthday=body.birthday,
        address=body.address,
    )
    session.add(contact)
    await session.commit()
    await session.refresh(contact)
    return contact


async def update_contact(
    contact_id: int, body: ContactModel, session: AsyncDBSession
) -> Contact | None:
    stmt = select(Contact).filter(Contact.id == contact_id)
    contact = await session.execute(stmt)
    contact = contact.scalar()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.address = body.address
        contact.updated_at = datetime.now()
        await session.commit()
    return contact


async def delete_contact(contact_id: int, session: AsyncDBSession) -> Contact | None:
    stmt = select(Contact).filter(Contact.id == contact_id)
    result = await session.execute(stmt)
    contact = result.scalar()
    if contact:
        await session.delete(contact)
        await session.commit()
    return contact