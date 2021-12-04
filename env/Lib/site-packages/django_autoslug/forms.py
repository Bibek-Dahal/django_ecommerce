import re
from django.forms.fields import SlugField
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

slug_re = re.compile(r'^[-\w\/]+$')
validate_autoslug = RegexValidator(slug_re, _(u"Enter a valid 'slug' consisting of letters, slash, numbers, underscores or hyphens."), 'invalid')

class AutoSlugField(SlugField):
    default_validators = [validate_autoslug]
