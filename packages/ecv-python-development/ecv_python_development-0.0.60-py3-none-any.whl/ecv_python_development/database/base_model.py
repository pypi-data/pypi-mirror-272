from __future__ import annotations

import os
from typing import Any, Callable, ClassVar, List, Literal, Optional, Pattern

from pydantic import BaseModel as PydanticBaseModel
from pydantic import (
    Field,
    PrivateAttr,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    create_model,
)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

from ._pynamodb.base import (
    PYDANTIC_PYNAMO_MAPPING,
    PynamoDBBaseModel,
    PynamoDBModel,
    UnicodeAttribute,
)

"""
check full documentation for fields at: https://docs.pydantic.dev/latest/concepts/fields/

"""


def field(
    default: Optional[str] = None,
    default_factory: Optional[Callable[..., Any]] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    examples: Optional[List[Any]] = None,
    frozen: Optional[bool] = False,
    exclude: Optional[bool] = False,
    pattern: Optional[Pattern[str]] = None,
    db_field: Optional[str] = None,
    is_hash_key: Optional[bool] = False,
    is_range_key: Optional[bool] = False,
    is_gsi_pk: Optional[bool] = False,
    is_gsi_sk: Optional[bool] = False,
    metadata: Optional[dict] = None,
) -> Any:

    json_extra_schema = {}

    if db_field is not None:
        json_extra_schema["db_field"] = db_field

    if is_hash_key == True:
        json_extra_schema["__hash_key__"] = True
    elif is_range_key == True:
        json_extra_schema["__range_key__"] = True

    if is_gsi_pk == True:
        json_extra_schema["__gsi_pk__"] = True
    elif is_gsi_sk == True:
        json_extra_schema["__gsi_sk__"] = True

    if metadata is not None:
        json_extra_schema = {**json_extra_schema, **metadata}

    parameters = {
        key: value
        for key, value in locals().items()
        if value is not None
        and key not in ["parameters", "is_hash_key", "is_range_key", "db_field"]
    }

    """
    These are the parameters I find to be extremely useful.
    
    I limited the parameters to this for easier readability. 
    
    This custom field is to enforce strict types.
    
    """
    return Field(**parameters, strict=True)


"""
Sample Implementation

from uuid import UUID, uuid4

class User(BaseModel):
    id: UUID = field(default_factory=uuid4)
    name: str = field(default="John Doe", min_length=1, description="name of the User")
    
user = User(name="warren")
print(user.json())

"""


class BaseModel(PydanticBaseModel):

    database_model: ClassVar[PynamoDBBaseModel] = None

    def __init__(
        self,
        db_type: Literal["dynamodb", "rds", "mongodb", None] = None,
        table_name: Optional[str] = None,
        **data,
    ) -> None:
        super().__init__(**data)

        if db_type is None:
            pass
        elif db_type == "dynamodb":
            self.__class__.set_pynamodb_model(table_name)
        else:
            raise Exception("Other database not yet supported")

    @classmethod
    def set_pynamodb_model(cls, table_name: str):
        attributes: dict = {}
        gsi_dict: dict[str, dict] = {}
        gsi_counter: int = 0

        for field_name, field_info in cls.model_fields.items():
            metadata = field_info.json_schema_extra["json_extra_schema"]
            if "__hash_key__" in metadata or "__range_key__" in metadata:
                if metadata.get("__hash_key__", False):
                    attributes[field_name] = UnicodeAttribute(
                        hash_key=True,
                        attr_name=metadata.get("db_field", field_name),
                    )
                else:
                    attributes[field_name] = UnicodeAttribute(
                        range_key=True,
                        attr_name=metadata.get("db_field", field_name),
                    )
            else:
                attributes[field_name] = PYDANTIC_PYNAMO_MAPPING.get(
                    field_info.annotation, UnicodeAttribute
                )(
                    null=field_info.exclude,
                    attr_name=metadata.get("db_field", field_name),
                )

                if "__gsi_pk__" in metadata:
                    gsi_counter += 1
                    gsi_dict[f"gsi_{gsi_counter}"] = {}

                    meta_class = type(
                        "Meta",
                        (),
                        {
                            "index_name": f"GSI{gsi_counter}",
                            "projection": AllProjection(),
                        },
                    )
                    gsi_dict[f"gsi_{gsi_counter}"]["Meta"] = meta_class

                    gsi_dict[f"gsi_{gsi_counter}"][
                        field_name
                    ] = PYDANTIC_PYNAMO_MAPPING.get(
                        field_info.annotation, UnicodeAttribute
                    )(
                        hash_key=True,
                        attr_name=metadata.get("db_field", field_name),
                    )

                    # attributes[f"GSI{gsi_counter}"] = gsi

                if "__gsi_sk__" in metadata:

                    if gsi_dict.get(f"gsi_{gsi_counter}", None):
                        gsi_dict[f"gsi_{gsi_counter}"][
                            field_name
                        ] = PYDANTIC_PYNAMO_MAPPING.get(
                            field_info.annotation, UnicodeAttribute
                        )(
                            range_key=True,
                            attr_name=metadata.get("db_field", field_name),
                        )

        for gsi in gsi_dict:
            index_class = type(
                f"GSI{gsi_counter}", (GlobalSecondaryIndex,), gsi_dict[gsi]
            )
            attributes[f"GSI{gsi_counter}"] = index_class()

        model_name = f"{cls.__name__}PynamoDBModel"
        PynamoDBModel = type(model_name, (PynamoDBBaseModel,), attributes)
        PynamoDBModel.Meta.table_name = table_name

        cls.database_model = PynamoDBModel

    def to_pynamodb_model(
        self, include: Optional[list | str] = "all", exclude: Optional[list] = []
    ) -> type[PynamoDBBaseModel]:
        return self.database_model(
            **self.model_serialize(include=include, exclude=exclude)
        )

    def model_serialize(
        self,
        include: Optional[list | str] = "all",
        exclude: Optional[list] = [],
        serialization_alias: Optional[bool] = True,
    ) -> dict[str, Any]:
        return self.model_dump(
            include=set(include) if type(include) == list else set(self.model_fields),
            exclude=set(exclude),
        )

    @classmethod
    def transform(
        cls, include: Optional[list | str] = "all", exclude: Optional[list] = []
    ) -> type[BaseModel]:

        base_fields = {**cls.model_fields, **BaseModel.model_fields}
        model_fields = {}

        for field_name, field_info in base_fields.items():
            if field_name in include or include == "all":
                model_fields[field_name] = (field_info.annotation, field_info)

            if field_name in exclude:
                model_fields.pop(field_name, None)

        model_name = f"{cls.__name__}Custom"

        new_model: BaseModel = create_model(
            __model_name=model_name,
            **model_fields,
            __base__=BaseModel,
        )

        return new_model
