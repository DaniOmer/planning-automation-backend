import asyncio
from datetime import datetime, timedelta
from random import randint, uniform

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.classrooms.model.classroom_model import Classroom
from src.apps.schedules.model.classes.classes_model import Classes
from src.apps.schedules.model.educational_courses.educational_courses_model import \
    EducationalCourses
from src.apps.schedules.model.subjects.subjects_model import Subjects
from src.apps.schedules.model.years_groups.years_groups_model import \
    YearsGroups
from src.config.database_service import AsyncSessionFactory

fake = Faker()

async def load_years_groups_data(session: AsyncSession, num: int = 5):
    """Insère 'num' years_groups avec des données aléatoires."""
    years_groups = [
        YearsGroups(
            name=fake.word().capitalize()
        )
        for _ in range(num)
    ]
    session.add_all(years_groups)
    await session.commit()
    await session.flush()  
    return years_groups

async def load_subjects_data(session: AsyncSession, num: int = 10):
    """Insère 'num' subjects avec des données aléatoires."""
    subjects = []
    for _ in range(num):
        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = start_date + timedelta(days=randint(30, 300))  
        subjects.append(Subjects(
            name=fake.word().capitalize(),
            hourly_volume=randint(10, 200),
            session_duration=uniform(1.0, 4.0),
            start_at=start_date,
            end_at=end_date
        ))
    session.add_all(subjects)
    await session.commit()

async def load_educational_courses_data(session: AsyncSession, num: int = 10):
    """Insère 'num' educational_courses avec des données aléatoires."""
    courses = []
    for _ in range(num):
        day = fake.date_this_year()
        courses.append(EducationalCourses(
            description=fake.sentence(nb_words=5),
            day=day
        ))
    session.add_all(courses)
    await session.commit()

async def load_classes_data(session: AsyncSession, years_groups_list, num: int = 10):
    """Insère 'num' classes en utilisant les years_groups déjà insérés.

    years_groups_list est la liste des objets YearsGroups retournés par load_years_groups_data.
    """
    years_groups_ids = [yg.id for yg in years_groups_list]

    classes_list = []
    for _ in range(num):
        yg_id = fake.random_element(elements=years_groups_ids)
        classes_list.append(Classes(
            name=fake.word().capitalize(),
            number_students=randint(20, 100),
            years_group_id=yg_id
        ))
    session.add_all(classes_list)
    await session.commit()

async def load_classroom_data(session: AsyncSession, num: int = 10):
    """Insère 'num' classes avec des données aléatoires."""
    classrooms = [
        Classroom(
            name=fake.word().capitalize(),
            capacity=fake.random_int(min=10, max=100)
        )
        for _ in range(num)
    ]
    session.add_all(classrooms)
    await session.commit()

async def main():
    async with AsyncSessionFactory() as session:
        print("Inserting YearsGroups...")
        years_groups_list = await load_years_groups_data(session, num=5)
        print("YearsGroups inserted successfully!")

        print("Inserting Subjects...")
        await load_subjects_data(session, num=10)
        print("Subjects inserted successfully!")

        print("Inserting EducationalCourses...")
        await load_educational_courses_data(session, num=10)
        print("EducationalCourses inserted successfully!")

        print("Inserting Classes...")
        await load_classes_data(session, years_groups_list, num=10)
        print("Classes inserted successfully!")

        print("Inserting Classrooms...")
        await load_classroom_data(session, num=10)
        print("Classrooms data inserted successfully!")

if __name__ == "__main__":
    asyncio.run(main())
