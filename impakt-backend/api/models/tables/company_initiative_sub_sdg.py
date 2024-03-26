from ..base import Base, CRUDMixin

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, ForeignKey


class CompanyInitiativeSubSdg(Base, CRUDMixin["CompanyInitiativeSubSdg"]):
    __name__ = "CompanyInitiativeSubSdg"

    initiative_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("CompanyInitiative.id"), primary_key=True
    )
    sub_sdg_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("SubSdg.id"), primary_key=True
    )
