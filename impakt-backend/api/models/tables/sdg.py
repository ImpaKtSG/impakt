from ..base import Base, CRUDMixin

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String


class Sdg(Base, CRUDMixin["Sdg"]):
    __name__ = "Sdg"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
                                                            
    
    