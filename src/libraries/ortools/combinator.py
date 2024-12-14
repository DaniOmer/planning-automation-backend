from ortools.sat.python import cp_model

class Combinator:
    def __init__(self, calendar, courses, session_duration, days_time_slot, nb_rooms):
        self.calendar = calendar
        self.courses = courses
        self.session_duration = session_duration
        self.days_time_slot = days_time_slot
        self.nb_rooms = nb_rooms

        self.model = cp_model.CpModel()
        self.start_hour, self.end_hour = days_time_slot
        self.course_days = [i for i, day in enumerate(calendar) if day['type'] == 'course']

    def create_sessions(self):
        """Creates sessions from courses."""
        sessions = []
        for course in self.courses:
            num_sessions = -(-course['hourly_volume'] // self.session_duration)
            for session_idx in range(num_sessions):
                sessions.append((course['id'], session_idx))
        return sessions

    def create_variables(self, sessions):
        """Creates decision variables."""
        x = {}
        for session in sessions:
            x[session] = {}
            for d in range(len(self.course_days)):
                for h in range(self.start_hour, self.end_hour):
                    var_name = f"x_s{session}_d{d}_h{h}"
                    x[session][(d, h)] = self.model.NewBoolVar(var_name)
        return x

    def add_session_constraints(self, sessions, x):
        """Ensures each session is scheduled exactly once."""
        for session in sessions:
            valid_slots = []
            for d in range(len(self.course_days)):
                for h in range(self.start_hour, self.end_hour - self.session_duration + 1):
                    valid_slots.append(x[session][(d, h)])
            self.model.Add(sum(valid_slots) == 1)

    def add_teacher_availability_constraints(self, sessions, x):
        """Ensures sessions respect teacher availability."""
        for session in sessions:
            course_id, _ = session
            course = next(c for c in self.courses if c['id'] == course_id)
            teacher_availability = course['teacher']['availability']

            for d in range(len(self.course_days)):
                day_index = self.course_days[d]
                day_date = self.calendar[day_index]['date']
                intervals = teacher_availability.get(day_date, [])

                for h in range(self.start_hour, self.end_hour):
                    var = x[session][(d, h)]
                    if h + self.session_duration > self.end_hour:
                        self.model.Add(var == 0)
                        continue

                    is_valid = any(start_h <= h and h + self.session_duration <= end_h for start_h, end_h in intervals)
                    if not is_valid:
                        self.model.Add(var == 0)

    def add_no_overlap_constraints(self, sessions, x):
        """Prevents overlapping sessions for the same teacher."""
        teacher_to_sessions = {}
        for session in sessions:
            course_id, _ = session
            course = next(c for c in self.courses if c['id'] == course_id)
            teacher_name = course['teacher']['name']
            teacher_to_sessions.setdefault(teacher_name, []).append(session)

        for teacher, teacher_sessions in teacher_to_sessions.items():
            for d in range(len(self.course_days)):
                for h in range(self.start_hour, self.end_hour):
                    vars_at_time = [x[session][(d, h)] for session in teacher_sessions]
                    self.model.Add(sum(vars_at_time) <= 1)


    def add_room_constraints(self, sessions, x):
        """Ensures the number of sessions does not exceed room availability."""
        for d in range(len(self.course_days)):
            for t in range(self.start_hour, self.end_hour):
                overlapping_vars = []
                for session in sessions:
                    for h in range(self.start_hour, self.end_hour - self.session_duration + 1):
                        if h <= t < h + self.session_duration:
                            overlapping_vars.append(x[session][(d, h)])
                self.model.Add(sum(overlapping_vars) <= self.nb_rooms)

    def solve(self):
        """Solves the model and returns the schedule."""
        sessions = self.create_sessions()
        x = self.create_variables(sessions)

        # Add constraints
        self.add_session_constraints(sessions, x)
        self.add_teacher_availability_constraints(sessions, x)
        self.add_no_overlap_constraints(sessions, x)
        self.add_room_constraints(sessions, x)

        # Solve the model
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)

        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            schedule = []
            for session in sessions:
                course_id, session_idx = session
                course = next(c for c in self.courses if c['id'] == course_id)

                for d in range(len(self.course_days)):
                    for h in range(self.start_hour, self.end_hour):
                        if solver.Value(x[session][(d, h)]) == 1:
                            day_index = self.course_days[d]
                            date = self.calendar[day_index]['date']
                            schedule.append({
                                "course_id": course_id,
                                "course": course['name'],
                                "day": date,
                                "start_time": h,
                                "end_time": h + self.session_duration,
                                "teacher": course['teacher']['name'],
                            })
            return schedule
        else:
            return {"status": solver.StatusName(status)}
