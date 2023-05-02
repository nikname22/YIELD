from django.db import models

class Project(models.Model):
    id_project = models.AutoField(primary_key=True)
    projeto = models.TextField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    tir_media = models.FloatField(null=True)
    total_captado = models.FloatField(null=True)
    vgv = models.FloatField(null=True)
