from sqlalchemy.orm import Session

from app.modules.itinerary.constants import (
    ACTIVITY_ORDER_ALREADY_EXISTS,
    ITINERARY_ACTIVITY_NOT_FOUND,
    ITINERARY_DAY_ALREADY_EXISTS,
    ITINERARY_NOT_FOUND,
)
from app.modules.itinerary.models import Itinerary, ItineraryActivity
from app.modules.itinerary.repository import (
    ItineraryActivityRepository,
    ItineraryRepository,
)
from app.modules.itinerary.schemas import (
    ItineraryActivityCreate,
    ItineraryActivityUpdate,
    ItineraryCreate,
    ItineraryUpdate,
)
from app.shared.exceptions.exceptions import (
    ResourceNotFoundException,
    ValidationException,
)


class ItineraryService:

    def __init__(
        self,
        repository: ItineraryRepository,
    ):
        self.repository = repository

    def get_all(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Itinerary]:
        return self.repository.get_by_trip_id(db, trip_id)

    def get_by_id(
        self,
        db: Session,
        itinerary_id: int,
    ) -> Itinerary:

        itinerary = self.repository.get_by_id(db, itinerary_id)

        if itinerary is None:
            raise ResourceNotFoundException(ITINERARY_NOT_FOUND)

        return itinerary

    def create(
        self,
        db: Session,
        request: ItineraryCreate,
    ) -> Itinerary:

        existing_days = self.repository.get_by_trip_id(
            db,
            request.trip_id,
        )

        if any(day.day_number == request.day_number for day in existing_days):
            raise ValidationException(ITINERARY_DAY_ALREADY_EXISTS)

        itinerary = Itinerary(**request.model_dump())

        return self.repository.create(db, itinerary)

    def update(
        self,
        db: Session,
        itinerary_id: int,
        request: ItineraryUpdate,
    ) -> Itinerary:

        itinerary = self.get_by_id(db, itinerary_id)

        if (
            request.day_number is not None
            and request.day_number != itinerary.day_number
        ):
            existing_days = self.repository.get_by_trip_id(
                db,
                itinerary.trip_id,
            )

            duplicate = any(
                day.id != itinerary.id
                and day.day_number == request.day_number
                for day in existing_days
            )

            if duplicate:
                raise ValidationException(
                    ITINERARY_DAY_ALREADY_EXISTS,
                )

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(itinerary, key, value)

        return self.repository.update(db, itinerary)

    def delete(
        self,
        db: Session,
        itinerary_id: int,
    ) -> None:

        itinerary = self.get_by_id(db, itinerary_id)

        self.repository.delete(db, itinerary)


class ItineraryActivityService:

    def __init__(
        self,
        repository: ItineraryActivityRepository,
    ):
        self.repository = repository

    def get_all(
        self,
        db: Session,
        itinerary_id: int,
    ) -> list[ItineraryActivity]:
        return self.repository.get_by_itinerary_id(
            db,
            itinerary_id,
        )

    def get_by_id(
        self,
        db: Session,
        activity_id: int,
    ) -> ItineraryActivity:

        activity = self.repository.get_by_id(
            db,
            activity_id,
        )

        if activity is None:
            raise ResourceNotFoundException(
                ITINERARY_ACTIVITY_NOT_FOUND,
            )

        return activity

    def create(
        self,
        db: Session,
        request: ItineraryActivityCreate,
    ) -> ItineraryActivity:

        print("=" * 80)
        print("CREATE ACTIVITY REQUEST")
        print("Request Type :", type(request))
        print("Request Data :", request.model_dump())

        existing_activities = self.repository.get_by_itinerary_id(
            db,
            request.itinerary_id,
        )

        print("Existing Activities:", len(existing_activities))

        if any(
            activity.activity_order == request.activity_order
            for activity in existing_activities
        ):
            raise ValidationException(
                ACTIVITY_ORDER_ALREADY_EXISTS,
            )

        activity = ItineraryActivity(**request.model_dump())

        print("ENTITY CREATED")
        print("Itinerary ID :", activity.itinerary_id)
        print("Title        :", activity.title)
        print("Activity Order:", activity.activity_order)

        saved = self.repository.create(
            db,
            activity,
        )

        print("ENTITY SAVED")
        print("ID          :", saved.id)
        print("=" * 80)

        return saved

    def update(
        self,
        db: Session,
        activity_id: int,
        request: ItineraryActivityUpdate,
    ) -> ItineraryActivity:

        activity = self.get_by_id(
            db,
            activity_id,
        )

        if (
            request.activity_order is not None
            and request.activity_order != activity.activity_order
        ):
            existing_activities = self.repository.get_by_itinerary_id(
                db,
                activity.itinerary_id,
            )

            duplicate = any(
                existing.id != activity.id
                and existing.activity_order == request.activity_order
                for existing in existing_activities
            )

            if duplicate:
                raise ValidationException(
                    ACTIVITY_ORDER_ALREADY_EXISTS,
                )

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for key, value in update_data.items():
            setattr(
                activity,
                key,
                value,
            )

        return self.repository.update(
            db,
            activity,
        )

    def delete(
        self,
        db: Session,
        activity_id: int,
    ) -> None:

        activity = self.get_by_id(
            db,
            activity_id,
        )

        self.repository.delete(
            db,
            activity,
        )