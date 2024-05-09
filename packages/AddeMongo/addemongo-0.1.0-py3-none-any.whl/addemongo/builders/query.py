from __future__ import annotations

from typing import Any, Callable


class QueryBuilder:
    def __init__(self) -> None:
        self.__query: dict[str, Any] = {}

    def set_equal(
        self, key: str, value: Any, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = value

        return self

    def set_not_equal(
        self, key: str, value: Any, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = {"$ne": value}

        return self

    def set_greater_than(
        self, key: str, value: Any, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = {"$gt": value}

        return self

    def set_greater_than_or_equal(
        self, key: str, value: Any, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = {"$gte": value}

        return self

    def set_less_than(
        self, key: str, value: Any, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = {"$lt": value}

        return self

    def set_less_than_or_equal(
        self, key: str, value: Any, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = {"$lte": value}

        return self

    def set_in(
        self, key: str, value: Any, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = {"$in": value}

        return self

    def set_not_in(
        self, key: str, value: Any, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = {"$nin": value}

        return self

    def set_regex(
        self,
        key: str,
        value: Any,
        case_sensivite: bool = True,
        condition: Callable[[], bool] = lambda: True,
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = {"$regex": value}

            if not case_sensivite:
                self.__query[key]["$options"] = "i"

        return self

    def set_not_regex(
        self,
        key: str,
        value: Any,
        case_sensivite: bool = True,
        condition: Callable[[], bool] = lambda: True,
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = {"$not": {"$regex": value}}

            if not case_sensivite:
                self.__query[key]["$options"] = "i"

        return self

    def set_element_match(
        self,
        key: str,
        query: QueryBuilder,
        condition: Callable[[], bool] = lambda: True,
    ) -> QueryBuilder:
        if condition():
            self.__query[key] = {"$elemMatch": query.build()}

        return self

    def set_or(
        self, *querys: QueryBuilder, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query["$or"] = [q.build() for q in querys]

        return self

    def set_and(
        self, *querys: QueryBuilder, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query["$and"] = [q.build() for q in querys]

        return self

    def set_nor(
        self, *querys: QueryBuilder, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query["$nor"] = [q.build() for q in querys]

        return self

    def update_query(
        self, query: dict[str, Any], condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query.update(query)

        return self

    def remove_key(
        self, key: str, condition: Callable[[], bool] = lambda: True
    ) -> QueryBuilder:
        if condition():
            self.__query.pop(key, None)

        return self

    def build(self):
        return self.__query
