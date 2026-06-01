from typing import TypedDict, Dict, Optional, List, Any
from pydantic import BaseModel, Field

# Metadata model
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

# Output model for functionality extraction
# class FunctionalityExtraction(BaseModel):
#     functionality: str = Field(description="Name der extrahierten Funktionalität")
#     description: str = Field(description="Beschreibung, was die Funktionalität in der App macht")
#     reasoning: str = Field(description=(
#         "Logische Herleitung, warum diese Funktion existiert, welche zwingend "
#         "ein direktes, wortwörtliches Zitat (in Anführungszeichen) aus dem "
#         "Originaltext als Textbeleg enthalten muss."
#     )
# )

# Output model for functionality extraction
# class FunctionalityExtraction(BaseModel):
#     functionality: str = Field(
#         description="Prägnanter Name der extrahierten Funktionalität (z.B. 'Zentrales Gesundheits-Dashboard')."
#     )
#     description: str = Field(
#         description="Detaillierte deutsche Beschreibung, was die Funktionalität in der App macht, inklusive genannter Einschränkungen oder Partner-Integrationen."
#     )
#     reasoning: str = Field(
#         description=(
#             "Analytische und logische Begründung, warum diese spezifische Funktion existiert. "
#             "Muss der Kausalität folgen: Welche technische/funktionale Eigenschaft lässt sich aus "
#             "den Schlüsselwörtern ableiten und warum MUSS das Feature aus diesem Grund existieren? "
#             "Keine reine Wiederholung des Textes und keine wörtlichen Zitate hier einfügen."
#         )
#     )
#     source_quotes: List[str] = Field(
#         description=(
#             "Eine Liste, die ausschließlich die originalen, unveränderten und wortwörtlichen "
#             "englischen Sätze oder Satzfragmente aus dem Quelltext enthält, die als direkter "
#             "Beweis für die Existenz dieses Features dienen."
#         )
# )

# class FunctionalityExtraction(BaseModel):
#     functionality: str = Field(
#         description="Prägnanter Name der extrahierten Funktionalität."
#     )
#     description: str = Field(
#         description="Detaillierte deutsche Beschreibung der App-Funktion, inklusive Einschränkungen oder Zusatzinfos."
#     )
#     reasoning: str = Field(
#         description=(
#             "Analytische Begründung, warum das Feature existiert. MUSS ein kurzes, "
#             "wesentliches Schlüsselwort oder Satzfragment (in Anführungszeichen) enthalten "
#             "und logisch herleiten, warum daraus die Existenz des Features folgt."
#         )
#     )
#     source_quotes: List[str] = Field(
#         description=(
#             "Liste der ausführlichen, originalen englischen Sätze aus dem Text. "
#             "Enthält sowohl den Kernbeleg für das Feature als auch Sätze mit "
#             "relevanten Zusatzinformationen oder Einschränkungen."
#         )
#     )

class FunctionalityExtraction(BaseModel):
    functionality: str = Field(
        description="A descriptive name for the extracted functionality."
    )
    description: str = Field(
        description="A detailed description of the app's features, including limitations or additional information."
    )
    reasoning: str = Field(
        description=(
            "Analytical justification for why the feature exists. MUST include a short, essential keyword or phrase (in quotation marks) and logically explain why this justifies the feature's existence."
        )
    )
    source_quotes: List[str] = Field(
        description=(
            "A list of the detailed, original sentences from the text. It includes both the key evidence for the feature and sentences containing relevant additional information or caveats."
        )
    )

class FunctionalityResult(BaseModel):
    features: List[FunctionalityExtraction] = Field(description="List of all extracted functionalities")

# State for the Pipeline
class PipelineState(TypedDict, total=False):

    # Raw input
    metadata: AppMetadata

    # App metadata
    pkg: str
    label: str
    description_long: str
    permissions_map: Dict[str, List[str]] = Field(default_factory=dict)

    # Results from stages
    functionality_result: FunctionalityResult

    # Execution config
    llm_model: str
    temperature: float
    storage_path: str
