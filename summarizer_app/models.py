from django.db import models

class File(models.Model):
    file = models.FileField(upload_to='files/')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name