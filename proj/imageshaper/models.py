from django.db import models


class ImgModel(models.Model):

    url = models.CharField(max_length=2048, null=True)
    fs_path = models.ImageField(upload_to='images/', null=True)
    width = models.CharField(max_length=9, null=True)
    height = models.CharField(max_length=9, null=True)

    def __repr__(self):
        return "<ImgModel: " + str(self.fs_path).split('/')[-1] + ">"
