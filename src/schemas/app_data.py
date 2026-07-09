from pydantic import BaseModel, Field
from typing import List, Optional

class Price(BaseModel):
    amount: float
    currency: str

class AppDate(BaseModel):
    date: str | None = None
    timestamp: int | None = None

class SDKInfo(BaseModel):
    target: Optional[int] = None
    min: Optional[int] = None

class Category(BaseModel):
    id: str
    name: str

class SupportInfo(BaseModel):
    website: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class DeveloperInfo(BaseModel):
    id: str
    name: str
    legalName: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class AppDescription(BaseModel):
    long: str = Field(..., description="Base64 encoded long description")
    short: str = Field(..., description="Base64 encoded short description")

class PermissionItem(BaseModel):
    category: str
    permissions: List[str]

class DataSafetyItem(BaseModel):
    category: str
    data: List[dict] 

class DataSafety(BaseModel):
    dataDeletable: bool
    dataEncrypted: bool
    independentlyReviewed: bool
    sharedData: List[DataSafetyItem] = []
    collectedData: List[DataSafetyItem] = []

class AppMetadata(BaseModel):
    pkg: str
    label: str = Field(..., description="Base64 encoded label")
    version: Optional[str] = None
    downloads: int
    rating: Optional[float] = None
    reviewCount: Optional[int] = None
    inAppPurchases: Optional[str] = None
    ageRating: str
    containsAds: bool
    price: Price
    published: AppDate
    updated: AppDate
    sdk: SDKInfo
    category: Category
    availableInDe: bool
    supportInfo: SupportInfo
    developerInfo: DeveloperInfo
    privacyPolicy: Optional[str] = None
    description: AppDescription
    permissions: List[PermissionItem] = []
    datasafety: Optional[DataSafety] = None