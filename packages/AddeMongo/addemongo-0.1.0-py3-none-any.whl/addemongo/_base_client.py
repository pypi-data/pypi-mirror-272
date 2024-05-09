from typing import TYPE_CHECKING, Any, Generic, Type

from pydantic import BaseModel as _PydanticBaseModel


from ._types import BM

if TYPE_CHECKING:
    from addemongo.connection import AddeMongoConnection


class AddeMongoBaseClient(Generic[BM]):
    def __init__(
        self,
        connection: 'AddeMongoConnection',
        database: str,
        collection: str,
        response_class: Type[BM],
    ) -> None:
        self.connection = connection
        self.database_name = database
        self.collection_name = collection
        self.response_class = response_class

    def projection_schema(self) -> dict[str, Any]:
        annotations: dict[str, Any] = {}
        self.__create_projection_schema(self.response_class, annotations)
        return annotations

    def __create_projection_schema(
        self, document: type[_PydanticBaseModel], base: dict[str, Any]
    ) -> dict[str, Any]:
        annotations = document.__annotations__.copy()
        for key, value in annotations.items():
            if issubclass(value, _PydanticBaseModel):
                base[key] = self.__create_projection_schema(value, {})
            else:
                base[key] = 1

        return base
