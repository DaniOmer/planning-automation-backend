import datetime
import random
from sqlalchemy import create_engine, text

# Connexion à la base de données
DATABASE_URL = "postgresql://planify:planify@localhost:5432/planify"
engine = create_engine(DATABASE_URL, echo=True)  # Affiche les requêtes SQL exécutées

# Génération des données
def insert_fixtures():
    with engine.connect() as connection:
        with connection.begin():  # Démarre une transaction explicite
            # Insertion dans la table user
            connection.execute(text("""
                INSERT INTO "user" (id, first_name, last_name, email, password, phone_number, role, created_by) VALUES 
                (1, 'Admin', 'Admin', 'admin@school.com', '$2b$12$.BiokufvfepfQBQerSR1/eUjapALF56E0ozSRre3ocYpqzmN4Glmq', '1234567890', 'admin', NULL),
                (2, 'John', 'Doe', 'john.doe@school.com', '$2b$12$.BiokufvfepfQBQerSR1/eUjapALF56E0ozSRre3ocYpqzmN4Glmq', '1234567891', 'teacher', 1),
                (3, 'Jane', 'Smith', 'jane.smith@school.com', '$2b$12$.BiokufvfepfQBQerSR1/eUjapALF56E0ozSRre3ocYpqzmN4Glmq', '1234567892', 'teacher', 1),
                (4, 'Alice', 'Brown', 'alice.brown@school.com', '$2b$12$.BiokufvfepfQBQerSR1/eUjapALF56E0ozSRre3ocYpqzmN4Glmq', '1234567893', 'teacher', 1),
                (5, 'Bob', 'White', 'bob.white@school.com', '$2b$12$.BiokufvfepfQBQerSR1/eUjapALF56E0ozSRre3ocYpqzmN4Glmq', '1234567894', 'teacher', 1),
                (6, 'Charlie', 'Davis', 'charlie.davis@school.com', '$2b$12$.BiokufvfepfQBQerSR1/eUjapALF56E0ozSRre3ocYpqzmN4Glmq', '1234567895', 'teacher', 1);
            """))

            # Insertion dans la table day_type
            connection.execute(text("""
                INSERT INTO "day_type" (id, type) VALUES 
                (1, 'Cours'),
                (2, 'Exam');
            """))

            # Insertion dans la table years_groups
            connection.execute(text("""
                INSERT INTO "years_groups" (id, name) VALUES 
                (1, '1IW'), (2, '2IW'), (3, '3IW'), (4, '4IW'), (5, '5IW'),
                (6, '1SR'), (7, '2SR'), (8, '3SR'), (9, '4SR'), (10, '5SR');
            """))

            # Génération des classes pour chaque years_group
            class_id = 1
            for group_id in range(1, 11):
                for i in range(1, 3):
                    class_name = f"{group_id}IW{i}" if group_id <= 5 else f"{group_id}SR{i}"
                    connection.execute(text("""
                        INSERT INTO "classes" (id, name, years_group_id, number_students) 
                        VALUES (:id, :name, :group_id, :number_students);
                    """).bindparams(id=class_id, name=class_name, group_id=group_id, number_students=20))
                    class_id += 1

            # Génération des jours ouvrables pour educational_courses
            start_date = datetime.date(2024, 9, 2)
            end_date = datetime.date(2024, 12, 31)
            holidays = [
                datetime.date(2024, 11, 1),  # Toussaint
                datetime.date(2024, 12, 25), # Noël
            ]
            current_date = start_date
            course_id = 1
            working_days = []
            while current_date <= end_date:
                if current_date.weekday() < 5 and current_date not in holidays:  # Exclure les samedis, dimanches et jours fériés
                    working_days.append(current_date)
                    connection.execute(text("""
                        INSERT INTO "educational_courses" (id, description, day) 
                        VALUES (:id, :description, :day);
                    """).bindparams(id=course_id, description=f"Course on {current_date}", day=current_date))
                    course_id += 1
                current_date += datetime.timedelta(days=1)

            # Insertion dans la table years_groups_educational_courses
            for group_id in range(1, 11):
                for course_id in range(1, len(working_days) + 1):  # Limiter aux IDs valides dans educational_courses
                    if group_id <= 5 and (25 <= course_id <= 30 or 70 <= course_id <= 75):
                        day_type = 'Exam'
                    elif group_id > 5 and (31 <= course_id <= 36 or 76 <= course_id <= 81):
                        day_type = 'Exam'
                    else:
                        day_type = 'Cours'
                    if course_id <= len(working_days):  # Vérifier que course_id existe dans educational_courses
                        connection.execute(text("""
                            INSERT INTO "years_groups_educational_courses" (years_group_id, educational_courses_id, day_type) 
                            VALUES (:group_id, :course_id, :day_type);
                        """).bindparams(group_id=group_id, course_id=course_id, day_type=day_type))

            # Insertion dans la table subjects
            connection.execute(text("""
                INSERT INTO "subjects" (id, name, hourly_volume, session_duration, start_at, end_at) VALUES 
                (1, 'React JS', 30, 2.0, '2024-09-01', '2024-12-31'),
                (2, 'CICD', 45, 1.5, '2024-09-15', '2024-12-15'),
                (3, 'Python', 40, 2.0, '2024-10-01', '2024-12-20'),
                (4, 'DevOps', 35, 2.0, '2024-09-10', '2024-11-30'),
                (5, 'Data Science', 50, 3.0, '2024-09-05', '2024-12-25');
            """))

            # Génération des disponibilités pour chaque enseignant
            for teacher_id in range(2, 7):  # Les enseignants ont des IDs de 2 à 6
                start_date = datetime.date(2024, 9, 1)
                while start_date < datetime.date(2024, 12, 31):
                    interval = random.randint(1, 15)  # Génère des intervalles de 1 à 15 jours
                    end_date = start_date + datetime.timedelta(days=interval - 1)
                    if end_date > datetime.date(2024, 12, 31):
                        end_date = datetime.date(2024, 12, 31)

                    connection.execute(text("""
                        INSERT INTO "availabilities" (users_id, comment, start_at, end_at, is_recurring) 
                        VALUES (:user_id, NULL, :start_at, :end_at, FALSE);
                    """).bindparams(user_id=teacher_id, start_at=start_date, end_at=end_date))

                    start_date = end_date + datetime.timedelta(days=1)  # Commence après la fin de la dernière disponibilité

            # Insertion dans la table assignments_subjects
            assignment_id = 1
            for teacher_id in range(2, 7):  # Les enseignants ont des IDs de 2 à 6
                subjects = random.sample(range(1, 6), random.randint(1, 2))  # 1 à 2 matières assignées
                classes = random.sample(range(1, 21), random.randint(1, 3))  # 1 à 3 classes assignées
                for subject_id in subjects:
                    for class_id in classes:
                        connection.execute(text("""
                            INSERT INTO "assignments_subjects" (id, classes_id, subjects_id, users_id, url_online) 
                            VALUES (:id, :class_id, :subject_id, :user_id, 'https://online-classroom.com');
                        """).bindparams(id=assignment_id, class_id=class_id, subject_id=subject_id, user_id=teacher_id))
                        assignment_id += 1

if __name__ == "__main__":
    insert_fixtures()
