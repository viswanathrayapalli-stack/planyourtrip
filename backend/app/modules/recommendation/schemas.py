from pydantic import BaseModel, ConfigDict


class RecommendedPlace(BaseModel):
    id: int
    name: str
    city: str
    state: str | None = None
    country: str
    place_type: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RecommendationResponse(BaseModel):
    destination_id: int
    destination_name: str
    total_recommendations: int
    recommendations: list[RecommendedPlace]
