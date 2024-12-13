from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database_service import get_db
from src.apps.schedules.services.availabilities.availabilities_service import (
    get_availabilities,
    get_availabilities_by_users_id,
    create_availability,
    update_availability,
    delete_availability,
    create_availability_from_csv
)
from src.apps.schedules.model.availabilities.availabilities_schema import (
    AvailabilityCreate,
    AvailabilityUpdate,
    AvailabilityResponse
)
from src.utils.csv_utils import validate_csv_columns
from datetime import datetime
import io
import pandas as pd

router = APIRouter(prefix="/availabilities")

@router.get("/", response_model=list[AvailabilityResponse])
async def read_availabilities(db: AsyncSession = Depends(get_db)):
    return await get_availabilities(db)

@router.get("/user/{users_id}", response_model=list[AvailabilityResponse])
async def read_availability_by_users_id(users_id: int, db: AsyncSession = Depends(get_db)):
    availability = await get_availabilities_by_users_id(db, users_id)
    if not availability:
        raise HTTPException(status_code=404, detail="No availabilities found for this user")
    return availability

@router.post("/", response_model=AvailabilityResponse)
async def create_new_availability(availability: AvailabilityCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_availability(db, availability)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{availability_id}", response_model=AvailabilityResponse)
async def update_existing_availability(availability_id: int, availability: AvailabilityUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated = await update_availability(db, availability_id, availability)
        if not updated:
            raise HTTPException(status_code=404, detail="Availability not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{availability_id}")
async def delete_existing_availability(availability_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_availability(db, availability_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Availability not found")
    return {"message": "Availability deleted successfully"}

@router.post("/import/{users_id}")
async def import_availabilities_from_csv(
    users_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db)
):
    """
    Import availability data from a CSV file.
    First column: date, second column: morning (boolean), third column: afternoon (boolean).
    If both morning and afternoon are true, set the availability from 9:30 to 17:30.
    """
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        required_columns = ['date', 'morning', 'afternoon']
        validate_csv_columns(df, required_columns)

        availabilities = []
        for _, row in df.iterrows():
            date = datetime.strptime(row['date'], '%Y-%m-%d').date()

            start_time = None
            end_time = None

            if row['morning'] and row['afternoon']:
                start_time = datetime.combine(date, datetime.strptime('09:30', '%H:%M').time())
                end_time = datetime.combine(date, datetime.strptime('17:30', '%H:%M').time())
            elif row['morning']:
                start_time = datetime.combine(date, datetime.strptime('09:30', '%H:%M').time())
                end_time = datetime.combine(date, datetime.strptime('12:00', '%H:%M').time())
            elif row['afternoon']:
                start_time = datetime.combine(date, datetime.strptime('14:00', '%H:%M').time())
                end_time = datetime.combine(date, datetime.strptime('17:30', '%H:%M').time())

            if start_time and end_time:
                availability = AvailabilityCreate(
                    users_id=users_id,
                    start_at=start_time,
                    end_at=end_time
                )
                availabilities.append(availability)

        for availability in availabilities:
            await create_availability_from_csv(db, availability)

        return {"detail": "Availabilities successfully imported from CSV"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process CSV: {str(e)}")