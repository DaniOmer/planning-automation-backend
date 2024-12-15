import csv
from io import StringIO
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.apps.schedules import YearsGroupsEducationalCourses

from src.apps.schedules.model.years_groups.years_groups_model import YearsGroups
from src.apps.schedules.services.years_groups.years_groups_service import YearsGroupService
from src.apps.schedules.model.educational_courses.educational_courses_model import EducationalCourses
from src.apps.schedules.model.educational_courses.educational_courses_schema import EducationalCourseCreate
from src.apps.schedules.services.educational_courses.educational_courses_service import EducationalCourseService

class YearsGroupsEducationalCoursesService:
    @staticmethod
    async def create_entry(data, session: AsyncSession):
        entry = YearsGroupsEducationalCourses(**data.dict())
        session.add(entry)
        await session.commit()
        await session.refresh(entry)
        return entry

    @staticmethod
    async def get_all_entries(session: AsyncSession):
        result = await session.execute(select(YearsGroupsEducationalCourses))
        return result.scalars().all()

    @staticmethod
    async def get_entry_by_ids(years_group_id, educational_courses_id, session: AsyncSession):
        result = await session.execute(
            select(YearsGroupsEducationalCourses).filter(
                YearsGroupsEducationalCourses.years_group_id == years_group_id,
                YearsGroupsEducationalCourses.educational_courses_id == educational_courses_id,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_entry(years_group_id, educational_courses_id, data, session: AsyncSession):
        entry = await YearsGroupsEducationalCoursesService.get_entry_by_ids(
            years_group_id, educational_courses_id, session
        )
        if entry:
            for key, value in data.dict().items():
                setattr(entry, key, value)
            await session.commit()
            await session.refresh(entry)
        return entry

    @staticmethod
    async def delete_entry(years_group_id, educational_courses_id, session: AsyncSession):
        entry = await YearsGroupsEducationalCoursesService.get_entry_by_ids(
            years_group_id, educational_courses_id, session
        )
        if entry:
            await session.delete(entry)
            await session.commit()
            return True
        return False

    async def upload_csv(
    years_group_id: int,
    file_content,
    session: AsyncSession
    ):
        csv_content = StringIO(file_content.decode())
        reader = csv.DictReader(csv_content)
        records_to_create = []

        try:
            async with session.begin():
                years_group = await YearsGroupService.get_years_group_by_id(years_group_id, session)
                if not years_group:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Years group with ID {years_group_id} not found. Please verify the provided ID."
                    )

                for idx, row in enumerate(reader, start=1):
                    try:
                        day_type = row["day_type"]
                        educational_course_day = row["day"]

                        try:
                            educational_course_day_date = datetime.strptime(educational_course_day, '%Y-%m-%d').date()
                        except ValueError:
                            raise ValueError(
                                f"Invalid date format on row {idx}: '{educational_course_day}'. Expected format: YYYY-MM-DD."
                            )

                        educational_course_day_data = EducationalCourseCreate(day=educational_course_day_date)
                        educational_course_day_date = await EducationalCourseService.get_or_create_educational_course(educational_course_day_data, session)

                        existing_record_qs = select(YearsGroupsEducationalCourses).where(
                            YearsGroupsEducationalCourses.years_group_id == years_group.id,
                            YearsGroupsEducationalCourses.educational_courses_id == educational_course_day_date.id
                        )
                        result = await session.execute(existing_record_qs)
                        existing_record = result.scalar_one_or_none()

                        if not existing_record:
                            ygec_record = YearsGroupsEducationalCourses(
                                day_type=day_type,
                                years_group_id=years_group.id,
                                educational_courses_id=educational_course_day_date.id
                            )
                            records_to_create.append(ygec_record)

                    except Exception as e:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Error processing CSV row {idx}: {e}"
                        )

                try:
                    session.add_all(records_to_create)
                    return records_to_create
                except IntegrityError as e:
                    raise HTTPException(
                        status_code=409,
                        detail=(
                            "A conflict occurred while inserting records. "
                            f"Possible duplicate entries in CSV or database."
                        )
                    )

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=409,
                detail=(
                    "A database integrity error occurred while processing the CSV. "
                    f"Ensure the records in the CSV file are unique."
                )
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {e}. Please check your input and try again."
            )

