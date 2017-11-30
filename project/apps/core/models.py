from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# ADDED.
import django.db.models.options as options


options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)


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

    # ES Mapping for Indexing.
    # ES6 tweaks:
    # Replaces 'string' with 'text'.
    # Replace 'index': 'not_analyzed' with 'index': False.
    # Replace 'store': 'yes' with 'store': True.
    # ISSUE:
    # TransportError(400, 'search_phase_execution_exception', 'Fielddata is disabled on text fields by default.
    # Set fielddata=true on [course_names | year_in_school] in order to load fielddata in memory by uninverting the inverted index.
    # Note that this can however use significant memory. Alternatively use a keyword field instead.')
    # UPDATE:
    # Tested using fielddata values, does not seem to eliminate bug (though erroring field changes as filddata boolean is set).
    # Tested using fields: {keyword: {type:}}} values, also doesn't work.
    # Using fielddata on course_names throws error when runnign indexing command:
    #     'Cannot enable fielddata on a [text] field that is not indexed: [course_names]'
    # Using keywords on course_names results in an error saying to use fielddate on course_names.
    # WTF...
    class Meta:
        es_index_name = 'django'
        es_type_name = 'Student'
        es_mapping = {
            'properties': {
                'university': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'text',
                            'index': False
                            # 'fielddata': True
                            # 'fields': {
                            #     'keyword': {
                            #       'type': 'keyword'
                            #     }
                            # }
                        }
                    }
                },
                'first_name': {
                    'type': 'text',
                    'index': False
                },
                'last_name': {
                    'type': 'text',
                    'index': False
                    },
                'age': {
                    'type': 'short'
                },
                'year_in_school': {
                    'type': 'text'
                    # 'fielddata': True
                    # 'fields': {
                    #     'keyword': {
                    #       'type': 'keyword'
                    #     }
                    # }
                },
                'name_complete': {
                    'type': 'completion',
                    'analyzer': 'simple',
                    'preserve_separators': True,
                    'preserve_position_increments': True,
                    'max_input_length': 50
                    # DISABLED TO SUCCEED IN BULK INDEXING.
                    # SEE ERRORS BELOW.
                    # 'payloads': True,
                },
                'course_names': {
                    'type': 'text',
                    'store': True,
                    'index': False,
                    'fielddata': True
                    # 'fields': {
                    #     'keyword': {
                    #       'type': 'keyword'
                    #     }
                    # }
                }
            }
        }

    def es_repr(self):
        data = {}
        mapping = self._meta.es_mapping
        data['_id'] = self.pk

        for field_name in mapping['properties'].keys():
            data[field_name] = self.field_es_repr(field_name)
        return data

    def field_es_repr(self, field_name):
        config = self._meta.es_mapping['properties'][field_name]
        if hasattr(self, 'get_es_%s' % field_name):
            field_es_value = getattr(self, 'get_es_%s' % field_name)()
        else:
            if config['type'] == 'object':
                related_object = getattr(self, field_name)
                field_es_value = {}
                field_es_value['_id'] = related_object.pk
                for prop in config['properties'].keys():
                    field_es_value[prop] = getattr(related_object, prop)
            else:
                field_es_value = getattr(self, field_name)
        return field_es_value

    def get_es_name_complete(self):
        return {
            "input": [self.first_name, self.last_name] #,
            # REMOVED - THREW ERRORS:
            # - failed to parse
            # -- unknown field name [output], must be one of [input, weight, contexts]
            # -- unknown field name [payload], must be one of [input, weight, contexts]
            # --- illegal_argument_exception
            #"output": "%s %s" % (self.first_name, self.last_name) #,
            #"payload": {"pk": self.pk},
        }

    def get_es_course_names(self):
        if not self.courses.exists():
            return []
        return [c.name for c in self.courses.all()]
