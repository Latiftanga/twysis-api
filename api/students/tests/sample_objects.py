from core.tests.faker import fake

from core.models import School, Programme
from students.models import Student, Guardian, House, Class


def get_school():
    return School.objects.create(
        name=fake.name(),
        address=fake.address(),
        city=fake.city(),
        region=fake.region()
    )


def get_programme():
    name = fake.name()
    return Programme.objects.create(
        name=name,
        short_name=name[0:4]
    )


def get_house(school):
    return House.objects.create(
        name=fake.name(),
        school=school
    )


def get_class(school):
    return Class.objects.create(
        programme=get_programme(),
        programme_division=fake.name()[0],
        year=fake.year(),
        school=school
    )


def get_student(school, **params):
    """create sample student """
    name = fake.name()
    return Student.objects.create(
        first_name=name.split(' ')[0],
        other_names=name.split(' ')[0],
        sex=fake.sex(),
        date_of_birth=fake.date(),
        place_of_birth=fake.city(),
        status=fake.student_status(),
        residential_address=fake.address(),
        hometown=fake.city(),
        nationality='Ghanaian',
        phone='0200000000',
        email=fake.email(),
        school=school,
        clas=get_class(school=school),
        house=get_house(school=school)
    )


def get_guardian(school):
    """create sample guardian """
    return Guardian.objects.create(
        name=fake.name,
        relation=fake.guardian_relation(),
        address=fake.address(),
        phone='0200000000',
        email=fake.email(),
        school=school
    )
