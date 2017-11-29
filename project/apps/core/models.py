from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# from django.contrib.contenttypes import generic


class University(models.Model):
    name = models.CharField(max_length=255, unique=True)

    # def __unicode__(self):            # Python 2.
    def __str__(self):                  # Python 3.
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)

    # def __unicode__(self):            # Python 2..
    def __str__(self):                  # Python 3.
        return self.name


class Student(models.Model):
    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )
    # note: incorrect choice in MyModel.create leads to creation of incorrect record
    year_in_school = models.CharField(
        max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    age = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # various relationships models
    university = models.ForeignKey(University, null=True, blank=True)
    courses = models.ManyToManyField(Course, null=True, blank=True)

    # def __unicode__(self):            # Python 2..
    def __str__(self):                  # Python 3.
        return (self.last_name + ', ' + self.first_name)
