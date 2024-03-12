from ..base import Base, CRUDMixin

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, ForeignKey


class CompanyDescription(Base, CRUDMixin["CompanyDescription"]):
    __name__ = "CompanyDescription"

    company_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("company.id"), primary_key=True
    )
    description: Mapped[str] = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"CompanyDescription(company_id={self.company_id!r}, description={self.description!r})"
