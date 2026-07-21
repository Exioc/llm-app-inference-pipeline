from pydantic import BaseModel, Field

class GroupFilterConfig(BaseModel):
    enabled: bool = Field(
        default=False, 
        description="Enables or disables the filter."
    )
    threshold: float = Field(
        default=0.5, 
        ge=0.0, 
        le=1.0, 
        description="Minimum probability (0.0 to 1.0) at which a group is retained."
    )

class PermissionFilterConfig(BaseModel):
    enabled: bool = Field(
        default=False, 
        description="Enables or disables the filter."
    )
    threshold: float = Field(
        default=0.5, 
        ge=0.0, 
        le=1.0, 
        description="Minimum probability (0.0 to 1.0) at which a permission is retained."
    )