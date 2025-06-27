from django.db import models
from django.contrib.auth.models import User


from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.

class Kategori(models.Model):
    nama = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "1. Kategori"

class Artikel(models.Model):
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    judul = models.CharField(max_length=200)
    konten = CKEditor5Field('Text', config_name='extends')
    gambar = models.ImageField(upload_to="artikel",blank=True, null=True)
    status = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.judul

    class Meta:
        verbose_name_plural = "2. Artikel"