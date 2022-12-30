import enum

class Role(enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class Gender(enum.Enum):
    masculine = "masculine"
    feminine = "feminine"
