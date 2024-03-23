from ..base import Base, CRUDMixin

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, ForeignKey, String


class SubSdg(Base, CRUDMixin["SubSdg"]):
    __name__ = "SubSdg"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sdg_id: Mapped[int] = mapped_column(Integer, ForeignKey('Sdg.id'))
    name: Mapped[str] = mapped_column(String, nullable=False)
                                                            
    
    