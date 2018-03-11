from django.db import models
from django.core.urlresolvers import reverse


class Institution(models.Model):
    name = models.CharField(max_length=200)
    phone = models.PositiveIntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app:institution_edit', kwargs={'pk': self.pk})