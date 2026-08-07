from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_favorite_service
from app.modules.favorite.schemas import FavoriteCreate, FavoriteResponse
from app.modules.favorite.service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.get(
    "/trips/{trip_id}",
    response_model=list[FavoriteResponse],
)
def get_favorites(
    trip_id: int,
    db: Session = Depends(get_db),
    service: FavoriteService = Depends(get_favorite_service),
):
    return service.get_by_trip_id(db, trip_id)


@router.post(
    "/",
    response_model=FavoriteResponse,
)
def create_favorite(
    request: FavoriteCreate,
    db: Session = Depends(get_db),
    service: FavoriteService = Depends(get_favorite_service),
):
    return service.create(db, request)


@router.delete(
    "/{favorite_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    service: FavoriteService = Depends(get_favorite_service),
):
    service.delete(db, favorite_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
