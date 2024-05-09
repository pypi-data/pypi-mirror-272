from __future__ import annotations

from typing import Any, Callable


class AggregationBuilder:
    def __init__(self):
        self.__aggregation_list: list[dict[str, Any]] = []

    def set_group(
        self,
        query: dict[str, Any],
        body: dict[str, Any],
        condition: Callable[[], bool] = lambda: True,
    ) -> "AggregationBuilder":
        if condition():
            self.__aggregation_list.append({"$group": {"_id": query, **body}})

        return self

    def set_match(
        self, query: dict[str, Any], condition: Callable[[], bool] = lambda: True
    ) -> "AggregationBuilder":
        if condition():
            self.__aggregation_list.append({"$match": query})

        return self

    def set_project(
        self, query: dict[str, Any], condition: Callable[[], bool] = lambda: True
    ) -> "AggregationBuilder":
        if condition():
            self.__aggregation_list.append({"$project": query})

        return self

    def set_sort(
        self, key: str, by: int, condition: Callable[[], bool] = lambda: True
    ) -> "AggregationBuilder":
        if condition():
            self.__aggregation_list.append({"$sort": {key: by}})

        return self

    def set_limit(
        self, limit: int, condition: Callable[[], bool] = lambda: True
    ) -> "AggregationBuilder":
        if condition():
            self.__aggregation_list.append({"$limit": limit})

        return self

    def set_skip(
        self, skip: int, condition: Callable[[], bool] = lambda: True
    ) -> "AggregationBuilder":
        if condition():
            self.__aggregation_list.append({"$skip": skip})

        return self

    def set_unwind(
        self, key: str, condition: Callable[[], bool] = lambda: True
    ) -> "AggregationBuilder":
        if condition():
            self.__aggregation_list.append({"$unwind": key})

        return self

    def set_lookup(
        self,
        key: str,
        from_collection: str,
        local_field: str,
        foreign_field: str,
        as_field: str,
        condition: Callable[[], bool] = lambda: True,
    ) -> "AggregationBuilder":
        if condition():
            self.__aggregation_list.append(
                {
                    "$lookup": {
                        "from": from_collection,
                        "localField": local_field,
                        "foreignField": foreign_field,
                        "as": as_field,
                    }
                }
            )

        return self

    def set_add_fields(
        self, query: dict[str, Any], condition: Callable[[], bool] = lambda: True
    ) -> "AggregationBuilder":
        if condition():
            self.__aggregation_list.append({"$addFields": query})

        return self

    def set_facet(
        self, query: dict[str, Any], condition: Callable[[], bool] = lambda: True
    ) -> "AggregationBuilder":
        if condition():
            self.__aggregation_list.append({"$facet": query})

        return self

    def build(self):
        return self.__aggregation_list
