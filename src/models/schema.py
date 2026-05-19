from typing import TypedDict, Dict, Optional, List, Any
from pydantic import BaseModel, Field

# Appmetadata Model

class Price(BaseModel):
    amount: float
    currency: str

class AppDate(BaseModel):
    date: str
    timestamp: int

class SDKInfo(BaseModel):
    target: int
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

class AppBaseModel(BaseModel):
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

class FeatureExtraction(BaseModel):
    """Einzelne Funktionalität mit Begründung."""
    functionality: str = Field(description="Name der extrahierten Funktionalität")
    description: str = Field(description="Kurze Beschreibung, was die Funktion tut")
    reasoning: str = Field(description="Textpassage und logische Herleitung, warum diese Funktion existiert")

class AppAnalysis(BaseModel):
    """Das finale JSON-Format."""
    features: List[FeatureExtraction] = Field(description="Liste aller extrahierten Funktionalitäten")

# PipelineState 
class PipelineState(TypedDict, total=False):

    # Raw input
    metadata: AppBaseModel

    # App metadata
    pkg: str
    label: str
    description_long: str
    permissions_map: Dict[str, List[str]] = Field(default_factory=dict)

    # Results from stages
    functionality_result: AppAnalysis

    # Execution config
    llm_model: str
    temperature: float
    storage_path: str
