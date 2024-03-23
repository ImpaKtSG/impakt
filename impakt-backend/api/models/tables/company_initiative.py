from ..base import Base, CRUDMixin

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum
import enum

class Impact(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class CompanyInitiative(Base, CRUDMixin["CompanyInitiative"]):
    __name__ = "CompanyInitiative"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("Company.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    key_stats: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    impact: Mapped[Enum] = mapped_column(Enum(Impact), nullable=True)
    justification: Mapped[str] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String, nullable=True)


    
    