# csp.py - Core CSP class that holds all the problem data

class TimetableCSP:
    """This class holds everything about our timetabling problem"""

    def __init__(self, courses, rooms, timeslots, conflicts, instructors):
        self.courses = courses
        self.rooms = rooms
        self.timeslots = timeslots
        self.conflicts = conflicts
        self.instructors = instructors

        # Generate initial domains (all possible (time, room) pairs for each course)
        self.domains = self.generate_domains()

    def generate_domains(self):
        """
        Creates the initial domain for each course.
        A domain is a list of possible (time_slot, room) pairs.
        We filter out obviously impossible ones right away.
        """
        domains = {}

        for course_id, course_info in self.courses.items():
            domains[course_id] = []

            # Step 1: find time slots that match the course duration
            valid_timeslots = []
            for slot_id, slot_info in self.timeslots.items():
                if slot_info['duration'] == course_info['duration']:
                    valid_timeslots.append(slot_id)

            # Step 2: find rooms that have required features AND enough capacity
            valid_rooms = []
            for room_id, room_info in self.rooms.items():
                # Check if room has all required features
                if course_info['features'].issubset(room_info['features']):
                    # Check if room is big enough
                    if room_info['capacity'] >= course_info['enrollment']:
                        valid_rooms.append(room_id)

            # Step 3: filter by instructor availability (if we have that data)
            instructor_name = course_info['instructor']
            if instructor_name in self.instructors:
                available_slots = self.instructors[instructor_name].get('available', [])
                if available_slots:
                    valid_timeslots = [ts for ts in valid_timeslots if ts in available_slots]

            # Step 4: combine valid timeslots and rooms into domain pairs
            for slot_id in valid_timeslots:
                for room_id in valid_rooms:
                    domains[course_id].append({
                        'time_slot': slot_id,
                        'room': room_id
                    })

        return domains

    def get_domain(self):
        """Just a getter for the domains"""
        return self.domains