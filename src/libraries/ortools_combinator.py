from ortools.sat.python import cp_model

class Combinator:
    def __init__(self, calendar, courses, session_duration, days_time_slot):
        """
        Initialise le solveur de planification.

        :param calendar: Liste des jours avec leur type et plage horaire.
        :param courses: Liste des cours avec volume horaire, plages temporelles, et enseignants.
        :param session_duration: Durée de chaque session (en heures).
        :param days_time_slot: Plage horaire des jours de type `course`.
        """
        self.calendar = calendar
        self.courses = courses
        self.session_duration = session_duration
        self.days_time_slot = days_time_slot
        self.model = cp_model.CpModel()

        # Filtrer les jours valides (de type `course`)
        self.course_days = [i for i, day in enumerate(calendar) if day['type'] == 'course']

    def solve(self):
        # Variables
        sessions = []
        day_vars = {}
        time_vars = {}

        # Générer les sessions de cours
        for course in self.courses:
            num_sessions = int(course['hourly_volume'] // self.session_duration)
            if num_sessions % self.session_duration != 0:
                num_sessions += 1
            for session_idx in range(num_sessions):
                sessions.append((course, session_idx))

        # Définir les variables pour chaque session
        for session in sessions:
            course, session_idx = session

            # Variable pour le jour (indice des jours de type `course`)
            day_vars[session] = self.model.NewIntVar(0, len(self.course_days) - 1, f"day_{course['name']}_{session_idx}")

            # Variable pour l'heure de début (entre 8h et 20h)
            start_hour = self.days_time_slot[0]
            end_hour = self.days_time_slot[1] - self.session_duration
            time_vars[session] = self.model.NewIntVar(start_hour, end_hour, f"time_{course['name']}_{session_idx}")

        # Contraintes
        for session in sessions:
            course, session_idx = session

            # Contraindre les sessions aux jours de type `course`
            day_idx = day_vars[session]
            self.model.AddElement(day_idx, [self.calendar[i]['type'] == 'course' for i in self.course_days], 1)

            # Respecter les plages horaires du jour
            start_hour = self.days_time_slot[0]
            end_hour = self.days_time_slot[1] - self.session_duration
            self.model.AddLinearConstraint(time_vars[session], start_hour, end_hour)

            # Respecter les disponibilités de l'enseignant
            teacher_availability = course['teacher']['availability']
            for available_range in teacher_availability:
                self.model.Add(time_vars[session] >= available_range[0])
                self.model.Add(time_vars[session] + self.session_duration <= available_range[1])

            # Plages temporelles des cours
            course_start = course['start_at']
            course_end = course['end_at']
            self.model.Add(time_vars[session] >= course_start)
            self.model.Add(time_vars[session] + self.session_duration <= course_end)

        # Optimisation (minimiser le conflit d'horaires, par exemple)
        self.model.Minimize(sum(time_vars.values()))

        # Résolution
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)

        # Extraction des résultats
        if status == cp_model.OPTIMAL:
            schedule = {}
            for session in sessions:
                course, session_idx = session
                day_idx = solver.Value(day_vars[session])
                time = solver.Value(time_vars[session])

                schedule[session] = {
                    "course": course['name'],
                    "day": self.calendar[self.course_days[day_idx]]['date'],
                    "start_time": f"{time}:00",
                    "teacher": course['teacher']['name'],
                }
            return schedule
        else:
            print("Aucune solution trouvée.")
            return None
