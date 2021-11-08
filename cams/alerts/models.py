from django.db import models


class Alert(models.Model):
    subject = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    snapshot = models.BinaryField()

    def __str__(self):
        return (self.subject)


class Detect(models.Model):
    subject = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    snapshot = models.BinaryField()

    def __str__(self):
        return (self.subject)