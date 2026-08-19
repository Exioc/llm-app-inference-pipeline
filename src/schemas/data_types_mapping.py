from typing import List, Dict
from pydantic import BaseModel, Field, ConfigDict

# Data model representing the details of a specific data type, including its category, name, and description.
class DataTypeDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    category: str = Field(
        description="The category of data, e.g., 'Financial info' or 'Location'."
    )
    data_type: str = Field(
        alias="dataType",
        description="The specific data type, e.g., 'User payment info'."
    )
    description: str = Field(
        description="Description of what this data type includes."
    )

# Data model representing the mapping between a permission and its associated data types.
class PermissionDataTypeMapping(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    permission: str = Field(
        description="The permission name, e.g., 'NFC_TRANSACTION_EVENT'."
    )
    data_types: List[DataTypeDetail] = Field(
        alias="dataTypes",
        description="List of associated data types for this permission."
    )

# Data model representing a list of permission-to-datatype mappings.
class PermissionDataTypeMappingList(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    mappings: List[PermissionDataTypeMapping] = Field(
        default_factory=list,
        description="A list of all permission-to-datatype mappings."
    )

    @property
    def as_dict(self) -> Dict[str, List[DataTypeDetail]]:
        return {item.permission: item.data_types for item in self.mappings}