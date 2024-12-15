import json
from datetime import datetime
from collections import defaultdict
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.schedules.model.availabilities.availabilities_model import Availabilities

class AvailabilityService:
    """Service for operations related to user availabilities"""

    @staticmethod
    async def get_availabilities_by_users_id(session: AsyncSession, user_id):
        c_user_id = int(user_id)
        query = select(Availabilities).where(Availabilities.users_id == c_user_id)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create_availability(session: AsyncSession, slots: list, user_id):
        try:
            c_user_id = int(user_id)
            c_slots = AvailabilityService.slots_datetime_to_str(slots)
            availability = Availabilities(
                slots=json.dumps(c_slots),
                users_id=c_user_id
            )
            session.add(availability)
            await session.commit()
            await session.refresh(availability)

            if availability.id is None:
                raise ValueError("Failed to create availability")

            return availability
        except SQLAlchemyError as e:
            await session.rollback()
            raise ValueError(f"An error occurred while creating availability: {e}")

    @staticmethod
    async def get_availability_by_id(
        session: AsyncSession, 
        availability_id: int
    ):
        try:
            query = select(Availabilities).where(Availabilities.id == availability_id)
            result = await session.execute(query)
            availability =  result.scalar_one_or_none()
            if not availability:
                raise ValueError(f"Availability with id {availability_id} does not exist")
            return availability
        except SQLAlchemyError as e:
            raise ValueError(f"An error occurred while retrieving availability: {e}")

    @staticmethod
    async def update_availability(
        session: AsyncSession, 
        availability_id: int, 
        slots: list,
        user_id
    ):
       try:
            c_user_id = int(user_id)
            c_slots = AvailabilityService.slots_datetime_to_str(slots)
            availability = await AvailabilityService.get_availability_by_id(session, availability_id)
            if not availability:
                raise ValueError(f"Availability with id {availability_id} does not exist")
            if availability.users_id != c_user_id:
                raise ValueError("User does not have permission to update this availability")
            
            availability.slots = json.dumps(c_slots)
            await session.commit()
            await session.refresh(availability)
            return availability
       except SQLAlchemyError as e:
            await session.rollback()
            raise ValueError(f"An error occurred while updating availability: {e}")

    @staticmethod
    async def delete_availability(session: AsyncSession, availability_id: int):
        try:
            availability = await AvailabilityService.get_availability_by_id(session, availability_id)
            if not availability:
                raise ValueError(f"Availability with id {availability_id} does not exist")
            await session.delete(availability)
            await session.commit()
            return availability
        except SQLAlchemyError as e:
            await session.rollback()
            raise ValueError(f"An error occurred while deleting availability: {e}")

    @staticmethod
    def slots_datetime_to_str(slots):
        for slot in slots:
            if isinstance(slot['start_at'], datetime):
                slot['start_at'] = slot['start_at'].isoformat()
            if isinstance(slot['end_at'], datetime):
                slot['end_at'] = slot['end_at'].isoformat()
        return slots

    @staticmethod
    def transform_slots(slots):
        t_slots = defaultdict(list)

        for slot in slots:
            date_str = slot['start_at'].strftime('%Y-%m-%d')
            start_minutes = slot['start_at'].hour * 60 + slot['start_at'].minute
            end_minutes = slot['end_at'].hour * 60 + slot['end_at'].minute
            t_slots[date_str].append((start_minutes, end_minutes))
        return t_slots
