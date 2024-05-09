from enum import Enum
from typing import Union, Dict, Optional, Literal

from pydantic import BaseModel, Field


class SchemaPrimitiveType(str, Enum):
    string = "string"
    number = "number"
    boolean = "boolean"


# Forward declare SchemaDataType because it references SchemaObject and SchemaArray
SchemaDataType = Union['SchemaPrimitiveType', 'SchemaObject', 'SchemaArray']


class SchemaObject(BaseModel):
    type: Literal["object"] = Field(default="object")
    properties: Dict[str, SchemaDataType]


class SchemaArray(BaseModel):
    type: Literal["array"] = Field(default="array")
    items: SchemaDataType


class CreateDatasetInput(BaseModel):
    """
    The name of the dataset.
    """
    name: str
    """
    The description of the dataset.
    """
    description: Optional[str] = None
    """
    The input schema of the dataset.
    """
    inputSchema: Dict[str, SchemaDataType]
    """
    The output schema of the dataset.
    """
    outputSchema: Dict[str, SchemaDataType]


class CreateFineTuneDatasetInput(BaseModel):
    """
    The name of the dataset.
    """
    name: str
    """
    The description of the dataset.
    """
    description: Optional[str] = None
