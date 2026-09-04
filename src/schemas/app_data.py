from typing import Any, List, Optional
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """Shared base model configuring camelCase alias parsing and snake_case attribute access."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Price(BaseSchema):
    amount: Optional[float] = None
    currency: Optional[str] = None


class AppDate(BaseSchema):
    date: Optional[str] = None
    timestamp: Optional[int] = None


class SDKInfo(BaseSchema):
    target: Optional[int] = None
    min: Optional[int] = None


class Category(BaseSchema):
    id: Optional[str] = None
    name: Optional[str] = None


class SupportInfo(BaseSchema):
    website: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class DeveloperInfo(BaseSchema):
    id: Optional[str] = None
    name: Optional[str] = None
    legal_name: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class AppDescription(BaseSchema):
    long: Optional[str] = Field(default=None, description="Base64 encoded long description")
    short: Optional[str] = Field(default=None, description="Base64 encoded short description")


class PermissionItem(BaseSchema):
    category: Optional[str] = None
    permissions: List[str] = Field(default_factory=list)


class DataSafetyItem(BaseSchema):
    category: Optional[str] = None
    data: List[dict[str, Any]] = Field(default_factory=list)


class DataSafety(BaseSchema):
    data_deletable: Optional[bool] = None
    data_encrypted: Optional[bool] = None
    independently_reviewed: Optional[bool] = None
    shared_data: List[DataSafetyItem] = Field(default_factory=list)
    collected_data: List[DataSafetyItem] = Field(default_factory=list)


# Main App Metadata Model
class AppMetadata(BaseSchema):
    # Required fields
    pkg: str
    label: str = Field(..., description="Base64 encoded label")
    description: AppDescription

    # Optional scalar & nested object fields
    version: Optional[str] = None
    downloads: Optional[int] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    in_app_purchases: Optional[str] = None
    age_rating: Optional[str] = None
    contains_ads: Optional[bool] = None
    price: Optional[Price] = None
    published: Optional[AppDate] = None
    updated: Optional[AppDate] = None
    sdk: Optional[SDKInfo] = None
    category: Optional[Category] = None
    available_in_de: Optional[bool] = None
    support_info: Optional[SupportInfo] = None
    developer_info: Optional[DeveloperInfo] = None
    privacy_policy: Optional[str] = None

    # Supports both 'dataSafety' (camelCase standard) and raw 'datasafety' keys from scrapers
    data_safety: Optional[DataSafety] = Field(
        default=None,
        validation_alias=AliasChoices("dataSafety", "datasafety"),
    )

    # Optional collection fields
    permissions: List[PermissionItem] = Field(default_factory=list)