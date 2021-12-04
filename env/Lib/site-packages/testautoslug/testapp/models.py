from django.db import models
from django_autoslug.fields import AutoSlugField

class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=('title',), recursive='parent')
    parent = models.ForeignKey('Page', blank=True, null=True)

    def __unicode__(self):
        return self.title
