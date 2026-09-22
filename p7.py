# 7. Course Registration Conflict Detector using Object-Oriented Programming Develop a Python application to help a college identify timetable conflicts when students register for multiple courses.

class  Course:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def conflicts_with(self, other_course):
        return not (self.end_time <= other_course.start_time or self.start_time >= other_course.end_time)

class Student:
    def __init__(self, name):
        self.name = name
        self.courses = []

    def register_course(self, course):
        for existing_course in self.courses:
            if course.conflicts_with(existing_course):
                print(f"Conflict detected: {course.name} conflicts with {existing_course.name}")
                return
        self.courses.append(course)
        print(f"{self.name} successfully registered for {course.name}")

# Example usage
course1 = Course("Math", 9, 11)
course2 = Course("Physics", 10, 12)
course3 = Course("Chemistry", 11, 13)

student1 = Student("vijay")
student1.register_course(course1)
student1.register_course(course2)
student1.register_course(course3)

student2 = Student("Ravi")
student2.register_course(course1)
student2.register_course(course2)
student2.register_course(course3)


