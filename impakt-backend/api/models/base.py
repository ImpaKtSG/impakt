from sqlalchemy import Column, and_
from sqlalchemy.orm import DeclarativeBase, ColumnProperty
from sqlalchemy.sql import update, select, delete
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Generic, Dict, Any, Tuple, TypeVar
from utils import AppExceptions, classproperty


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy declarative models in the application.

    This class provides a default __tablename__ attribute that is derived from the class name.

    Attributes:
        __name__ (str): The name of the class, which is used to generate the table name.
    """

    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        """Generates the table name from the class name.

        Returns:
            str: The table name equivalent to the class name.
        """
        return self.__name__


Table = TypeVar("Table", bound=Base)


def _generate_where_clause(cls: Table, data: Dict[str, Any]):
    """Generates a WHERE clause from a dictionary of column-value pairs.

    Args:
        cls (Table): The SQLAlchemy table class.
        data (Dict[str, Any]): A dictionary where the keys are column names and the values are the values to filter by.

    Returns:
        The WHERE clause as a SQLAlchemy boolean expression.
    """
    return and_(*[getattr(cls, k) == v for k, v in data.items()])


class CRUDMixin(Generic[Table]):

    @classproperty
    def pk(cls) -> Tuple[Column]:
        """Gets the primary key columns of the table.

        This class property returns a tuple of SQLAlchemy Column objects representing the primary key columns of the table.

        Raises:
            AppExceptions.GENERIC_EXCEPTION: If no primary key is found for the table.

        Returns:
            Tuple[Column]: The primary key columns of the table.
        """
        inspected = inspect(cls)
        if inspected is None:
            raise AppExceptions.GENERIC_EXCEPTION("No primary key found")

        return tuple(inspected.primary_key)

    @classproperty
    def columns(cls) -> Tuple[ColumnProperty]:
        """Gets the columns of the table.

        This class property returns a tuple of SQLAlchemy ColumnProperty objects representing the columns of the table.

        Raises:
            AppExceptions.GENERIC_EXCEPTION: If no columns are found for the table.

        Returns:
            Tuple[ColumnProperty]: The columns of the table.
        """
        inspected = inspect(cls)
        if inspected is None:
            raise AppExceptions.GENERIC_EXCEPTION("No columns found")

        return tuple(inspected.columns)

    @classmethod
    async def create(cls: Table, session: AsyncSession, data: Dict[str, Any]) -> Table:
        """Creates a new instance of the table and adds it to the session.

        This class method creates a new instance of the table with the data provided, adds it to the session, and commits the session. If an IntegrityError occurs, it rolls back the session and raises an appropriate exception.

        Args:
            cls (Table): The SQLAlchemy table class.
            session (AsyncSession): The SQLAlchemy session.
            data (Dict[str, Any]): A dictionary where the keys are column names and the values are the values to set.

        Raises:
            AppExceptions.RESOURCE_NOT_FOUND: If a ForeignKeyViolationError occurs.
            AppExceptions.RESOURCE_EXISTS: If a UniqueViolationError occurs.
            AppExceptions.GENERIC_EXCEPTION: If any other IntegrityError occurs.

        Returns:
            Table: The new instance of the table.
        """
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
    async def get(cls: Table, session: AsyncSession, data: Dict[str, Any]) -> Table:
        """Retrieves a single instance of the table based on the provided filters.

        This class method generates a WHERE clause from the provided data, executes a SELECT statement with the WHERE clause, and returns the first result. If an IntegrityError occurs, it raises an appropriate exception.

        Args:
            cls (Table): The SQLAlchemy table class.
            session (AsyncSession): The SQLAlchemy session.
            data (Dict[str, Any]): A dictionary where the keys are column names and the values are the values to filter by.

        Raises:
            AppExceptions.GENERIC_EXCEPTION: If an IntegrityError occurs.
            AppExceptions.RESOURCE_NOT_FOUND: If no result is found.

        Returns:
            Table: The first instance of the table that matches the filters.
        """

        try:
            filters = _generate_where_clause(cls, data)
            stmt = select(cls).where(filters)
            result = await session.execute(stmt)
            ret = result.scalar()

        except IntegrityError as e:
            raise AppExceptions.GENERIC_EXCEPTION(e.detail) from e
        if ret is None:
            raise AppExceptions.RESOURCE_NOT_FOUND
        return ret

    @classmethod
    async def get_all(cls: Table, session: AsyncSession) -> Table:
        """Retrieves all instances of the table.

        This class method executes a SELECT statement for all rows in the table and returns the results. If no results are found, it raises an appropriate exception.

        Args:
            cls (Table): The SQLAlchemy table class.
            session (AsyncSession): The SQLAlchemy session.

        Raises:
            AppExceptions.RESOURCE_NOT_FOUND: If no results are found.

        Returns:
            Table: All instances of the table.
        """
        stmt = select(cls)
        exec = await session.execute(stmt)
        ret = exec.all()
        if ret is None:
            raise AppExceptions.RESOURCE_NOT_FOUND
        return ret

    @classmethod
    async def update(
        cls: Table, session: AsyncSession, pk: Dict[str, Any], data: Dict[str, Any]
    ) -> Table:
        """Updates an existing instance of the table based on the provided primary key and data.

        This class method generates a WHERE clause from the provided primary key, executes an UPDATE statement with the WHERE clause and the provided data, and returns the updated instance. If an IntegrityError occurs, it rolls back the session and raises an appropriate exception.

        Args:
            cls (Table): The SQLAlchemy table class.
            session (AsyncSession): The SQLAlchemy session.
            pk (Dict[str, Any]): A dictionary where the keys are primary key column names and the values are the values to filter by.
            data (Dict[str, Any]): A dictionary where the keys are column names and the values are the new values to set.

        Raises:
            AppExceptions.RESOURCE_NOT_FOUND: If a ForeignKeyViolationError occurs.
            AppExceptions.RESOURCE_EXISTS: If a UniqueViolationError occurs.
            AppExceptions.GENERIC_EXCEPTION: If any other IntegrityError occurs.

        Returns:
            Table: The updated instance of the table.
        """
        try:
            filters = _generate_where_clause(cls, pk)
            stmt = update(cls).where(filters).values(**data).returning(cls)
            result = await session.execute(stmt)
            ret = result.scalar_one()
        except IntegrityError as e:

            await session.rollback()
            if str(e).find("ForeignKeyViolationError") != -1:
                raise AppExceptions.RESOURCE_NOT_FOUND from e
            elif str(e).find("UniqueViolationError") != -1:
                raise AppExceptions.RESOURCE_EXISTS from e
            raise AppExceptions.GENERIC_EXCEPTION(e.detail) from e

        return ret

    @classmethod
    async def delete(cls: Table, session: AsyncSession, pk: Dict[str, Any]) -> Table:
        """Deletes an existing instance of the table based on the provided primary key.

        This class method generates a WHERE clause from the provided primary key, executes a DELETE statement with the WHERE clause, and returns the deleted instance. If an IntegrityError occurs, it rolls back the session and raises an appropriate exception.

        Args:
            cls (Table): The SQLAlchemy table class.
            session (AsyncSession): The SQLAlchemy session.
            pk (Dict[str, Any]): A dictionary where the keys are primary key column names and the values are the values to filter by.

        Raises:
            AppExceptions.RESOURCE_NOT_FOUND: If a ForeignKeyViolationError occurs.
            AppExceptions.RESOURCE_EXISTS: If a UniqueViolationError occurs.
            AppExceptions.GENERIC_EXCEPTION: If any other IntegrityError occurs.

        Returns:
            Table: The deleted instance of the table.
        """
        try:
            filters = _generate_where_clause(cls, pk)
            stmt = delete(cls).where(filters)
            ret = await session.execute(stmt)
        except IntegrityError as e:

            await session.rollback()
            if str(e).find("ForeignKeyViolationError") != -1:
                raise AppExceptions.RESOURCE_NOT_FOUND from e
            elif str(e).find("UniqueViolationError") != -1:
                raise AppExceptions.RESOURCE_EXISTS from e
            raise AppExceptions.GENERIC_EXCEPTION(e.detail) from e

    def __repr__(self):
        """Generates a string representation of the instance of the table.

        Returns:
            str: A string representation of the instance of the table.
        """
        return f"{self.__name__}({', '.join(f'{c.name}={getattr(self, c.name)!r}' for c in self.columns)})"
