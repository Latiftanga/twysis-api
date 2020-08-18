import uuid
from core.tests.faker import fake

from core.models import School, Programme, House
from students.models import Student, Guardian


def get_school():
    return School.objects.create(
        name=str(uuid.uuid4())[:9],
        address=fake.address(),
        city=fake.city(),
        region=fake.region()
    )


def get_programme():
    name = str(uuid.uuid4())[:7]
    return Programme.objects.create(
        name=name,
        code=name[0:2]
    )


def get_house(school):
    return House.objects.create(
        name=str(uuid.uuid4())[:4],
        school=school
    )


def get_student(school):
    """create sample student """
    name = fake.name()
    return Student.objects.create(
        admission_id=fake.name(),
        first_name=name.split(' ')[0],
        last_name=name.split(' ')[-1],
        sex=fake.sex(),
        date_of_birth=fake.date(),
        place_of_birth=fake.city(),
        status=fake.student_status(),
        residential_address=fake.address(),
        hometown=fake.city(),
        nationality='Ghanaian',
        phone='0200000000',
        email=fake.email(),
        school=school
    )


def get_guardian(school):
    """create sample guardian """
    return Guardian.objects.create(
        name=fake.name(),
        relation=fake.guardian_relation(),
        address=fake.address(),
        phone='0200000000',
        email=fake.email(),
        school=school
    )


def get_student_dafault_payload(**params):
    """Return sample student payload for only required fields"""
    name = fake.name()
    defaults = {
        'admission_id': fake.name(),
        'first_name': name.split(' ')[0],
        'last_name': name.split(' ')[1],
        'sex': fake.sex(),
        'status': fake.student_status(),
        'date_of_birth': fake.date(),
        'place_of_birth': fake.city(),
        'hometown': fake.city(),
        'residential_address': fake.address(),
        'nationality': 'Ghanaian',
    }
    defaults.update(params)
    return defaults


def create_student(school, **params):
    """Create a sample recipe and return it"""
    defaults = {
        'admission_id': fake.name(),
        'first_name': fake.name().split(' ')[0],
        'last_name': fake.name().split(' ')[-1],
        'sex': fake.sex(),
        'status': fake.student_status(),
        'date_of_birth': fake.date(),
        'place_of_birth': fake.city(),
        'hometown': fake.city(),
        'residential_address': fake.address(),
        'nationality': 'Ghanaian'
    }
    defaults.update(params)  # Overwrite or add addtional key/values

    return Student.objects.create(school=school, **defaults)
