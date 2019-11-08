

from django.db import models


class Event(models.Model):
    date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    checkin_count = models.IntegerField( null=True, blank=True)
    ticket_count = models.IntegerField( null=True, blank=True)
    session_count = models.IntegerField( null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '{} {} {}'.format(self.date, self.name, self.country)


