from django.db import models

from core.models import School, Programme


class Class(models.Model):
    """Students group object"""

    YEAR_IN_SCHOOL_CHOICES = [
        (1, 'Year 1'),
        (2, 'Year 2'),
        (3, 'Year 3'),
        (4, 'Year 4'),
        (5, 'Year 5'),
        (6, 'Year 6')
    ]

    programme = models.ForeignKey(
        Programme,
        related_name='classes',
        on_delete=models.CASCADE
    )
    programme_division = models.CharField(max_length=255)
    year = models.IntegerField(choices=YEAR_IN_SCHOOL_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='classes',
        null=True
    )

    @property
    def name(self):
        return f'{self.programme.short_name} {self.year} {self.programme_division}'

    def __str__(self):
        return self.name
