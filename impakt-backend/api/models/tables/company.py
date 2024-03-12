from ..base import Base, CRUDMixin

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String
from ..client import make_session, engine


class Company(Base, CRUDMixin["Company"]):
    __name__ = "Company"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    stock_ticker: Mapped[str] = mapped_column(String, nullable=True)
    website: Mapped[str] = mapped_column(String, nullable=True)

    @classmethod
    async def test(cls):

        async with make_session(engine) as s:
            ret = await cls.create(
                s, data={"name": "test", "stock_ticker": "test", "website": "test"}
            )
            print(await cls.get(s, data={"id": ret.id}))
            print(await cls.get_all(s))
            await s.close()

        return ret

    def __repr__(self):
        return f"Company(id={self.id!r}, name={self.name!r}, stock_ticker={self.stock_ticker!r}, website={self.website!r})"
