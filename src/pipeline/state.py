from typing import TypedDict, Dict, Optional, List, Any
from pydantic import BaseModel, Field

from src.schemas.app_metadata import AppMetadata
from src.schemas.permissions_groups import PermissionGroupsResult
from src.schemas.functionality import FunctionalityResult

# # App Metadata Schema
# class Price(BaseModel):
#     amount: float
#     currency: str

# class AppDate(BaseModel):
#     date: str | None = None
#     timestamp: int | None = None

# class SDKInfo(BaseModel):
#     target: int
#     min: Optional[int] = None

# class Category(BaseModel):
#     id: str
#     name: str

# class SupportInfo(BaseModel):
#     website: Optional[str] = None
#     email: Optional[str] = None
#     address: Optional[str] = None

# class DeveloperInfo(BaseModel):
#     id: str
#     name: str
#     legalName: Optional[str] = None
#     website: Optional[str] = None
#     email: Optional[str] = None
#     address: Optional[str] = None
#     phone: Optional[str] = None

# class AppDescription(BaseModel):
#     long: str = Field(..., description="Base64 encoded long description")
#     short: str = Field(..., description="Base64 encoded short description")

# class PermissionItem(BaseModel):
#     category: str
#     permissions: List[str]

# class DataSafetyItem(BaseModel):
#     category: str
#     data: List[dict] 

# class DataSafety(BaseModel):
#     dataDeletable: bool
#     dataEncrypted: bool
#     independentlyReviewed: bool
#     sharedData: List[DataSafetyItem] = []
#     collectedData: List[DataSafetyItem] = []

# class AppMetadata(BaseModel):
#     pkg: str
#     label: str = Field(..., description="Base64 encoded label")
#     version: Optional[str] = None
#     downloads: int
#     rating: Optional[float] = None
#     reviewCount: Optional[int] = None
#     inAppPurchases: Optional[str] = None
#     ageRating: str
#     containsAds: bool
#     price: Price
#     published: AppDate
#     updated: AppDate
#     sdk: SDKInfo
#     category: Category
#     availableInDe: bool
#     supportInfo: SupportInfo
#     developerInfo: DeveloperInfo
#     privacyPolicy: Optional[str] = None
#     description: AppDescription
#     permissions: List[PermissionItem] = []
#     datasafety: Optional[DataSafety] = None

# # Functionality Extraction Schema
# class FunctionalityExtractionContainer(BaseModel):
#     functionality: str = Field(
#         description="A clear, meaningful, and distinct name for the extracted feature or functionality in English."
#     )
#     description: str = Field(
#         description=(
#             "A highly detailed, comprehensive English description of what the feature does, "
#             "including its full scope, limitations, restrictions, and specific conditions mentioned in the text."
#         )
#     )
#     reasoning: str = Field(
#         description=(
#             "A concise explanation proving why this feature exists by connecting one or multiple clues "
#             "from the text. Aggregated Deduction Rule: Compile all relevant observations (Fact 1, Fact 2, ..., Fact N) "
#             "to justify your conclusion. This proof must be either:\n"
#             "1. DIRECT EVIDENCE: Show how the combination of explicit text mentions directly yields the feature.\n"
#             "2. LOGICAL INFERENCE: Show how multiple indirect contextual facts logically interlock to imply the "
#             "unspoken feature (e.g., Fact 1: 'stay in touch' + Fact 2: 'share images' -> infers a multimedia messaging tool exists).\n"
#             "Do not invent underlying software architecture, APIs, or unmentioned technical components. "
#             "Focus strictly on mapping the documented facts to the feature's existence."
#         )
#     )
#     source_quotes: List[str] = Field(
#         description=(
#             "A list of the original, unaltered sentences from the text that served as the basis or context for this extraction."
#         )
#     )

# class FunctionalityResult(BaseModel):
#     features: List[FunctionalityExtractionContainer] = Field(
#         description=(
#             "List of all extracted features. Granularity rule: Bundle sub-features that belong together "
#             "and cannot stand alone (e.g., chat messaging + typing indicators). Isolate into a separate feature "
#             "ONLY if a completely distinct capability or unique interaction method (e.g., voice/video calling) "
#             "is introduced."
#         )
#     )

# # Group Permissions Schema
# class PermissionGroupsContainer(BaseModel):
#     title: str = Field(
#         description="The distinct English name of the extracted app feature."
#     )
#     description: str = Field(
#         description="The detailed, multi-sentence description of what the feature does."
#     )
#     groups: List[str] = Field(
#         default_factory=list, 
#         description=(
#             "The inferred Android permission groups required for this feature "
#             "(e.g., STORAGE, CAMERA, LOCATION). Initialized as empty, filled by the filter node."
#         )
#     )

# class PermissionGroupsResult(BaseModel):
#     features: List[PermissionGroupsContainer]

# class SingleFeatureGroup(BaseModel):
#     groups: List[str] = Field(
#         description=(
#             "Select the relevant Android permission categories for this specific feature. "
#             "Options: [STORAGE, CAMERA, LOCATION, NETWORK, AUDIO, CONTACTS]. "
#             "If no permissions are required, return ['NONE']."
#         )
#     )

# State for the Pipeline
class PipelineState(TypedDict, total=False):

    # Raw input
    metadata: AppMetadata

    # App metadata
    pkg: str
    label: str
    description_long: str
    permissions_map: Dict[str, List[str]] = Field(default_factory=dict)

    # Results from functionality extraction 
    functionality_result: FunctionalityResult

    # Result from group permission filter
    group_permissions_result: PermissionGroupsResult
    current_group_index: int

    # Execution config
    llm_model: str
    temperature: float
    storage_path: str
