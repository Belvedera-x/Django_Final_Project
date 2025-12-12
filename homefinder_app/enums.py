from enum import StrEnum



class Gender(StrEnum):
    male = "Male"
    female = "Female"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]



class Role(StrEnum):
    owner = "owner"
    tenant = "tenant"
    admin = "admin"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]


class HousingType(StrEnum):
    apartment = "Apartment"
    house = "House"
    studio = "Studio"
    room = "Room"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]


class BookingStatus(StrEnum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    rejected = "rejected"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]