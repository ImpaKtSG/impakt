from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import update, select, delete
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Generic, Dict, Any, Tuple, TypeVar
from api.utils import AppExceptions, classproperty


class Base(DeclarativeBase):

    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


Table = TypeVar("Table", bound=Base)


class CRUDMixin(Generic[Table]):

    @classproperty
    def pk(cls) -> Tuple[str]:
        inspected = inspect(cls)
        if inspected is None:
            raise AppExceptions.GENERIC_EXCEPTION("No primary key found")

        return inspected.primary_key

    @classmethod
    async def create(cls: Table, session: AsyncSession, data: Dict[str, Any]) -> Table:
        try:

            instance = cls(**data)
            session.add(instance)
        except IntegrityError as e:
            await session.rollback()
            if str(e).find("ForeignKeyViolationError") != -1:
                raise AppExceptions.RESOURCE_NOT_FOUND from e
            elif str(e).find("UniqueViolationError") != -1:
                raise AppExceptions.RESOURCE_EXISTS from e

            raise AppExceptions.GENERIC_EXCEPTION(e.detail) from e
        await session.commit()
        return instance

    @classmethod
    async def get(cls: Table, session: AsyncSession, query) -> Table:

        try:
            stmt = select(cls).where(query)
            result = await session.execute(stmt)
            ret = result.scalar()

        except IntegrityError as e:
            raise AppExceptions.GENERIC_EXCEPTION(e.detail) from e
        if ret is None:
            raise AppExceptions.RESOURCE_NOT_FOUND
        return ret

    @classmethod
    async def get_all(cls: Table, session: AsyncSession) -> Table:
        ret = await session.get(cls)
        if ret is None:
            raise AppExceptions.RESOURCE_NOT_FOUND
        return ret

    @classmethod
    async def update(
        cls: Table, session: AsyncSession, pk: Any, data: Dict[str, Any]
    ) -> Table:
        stmt = update(cls).where(cls.id == pk).values(**data).returning(cls)
