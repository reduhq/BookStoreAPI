import enum

class Role(enum.Enum):
    admin = "admin"
    writer = "writer"
    reader = "reader"

class Gender(enum.Enum):
    masculine = "masculine"
    feminine = "feminine"
