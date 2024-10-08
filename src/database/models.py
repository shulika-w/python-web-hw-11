from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(79), nullable=False)
    last_name: Mapped[str] = mapped_column(String(79), nullable=False)
    email: Mapped[str] = mapped_column(String(79), nullable=True, unique=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=True, unique=True)
    birthday: Mapped[date] = mapped_column(Date())
    address: Mapped[str] = mapped_column(String(150), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name