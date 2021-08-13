from django.db import models


class Note(models.Model):
    input_text = models.TextField()
    times = models.TextField()
    dates = models.TextField()

    def __str__(self):
        return str(self.input_text) + " / " + str(self.times) + " " + str(self.dates)

