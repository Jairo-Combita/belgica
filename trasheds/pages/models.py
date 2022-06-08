from django.db import models
from ckeditor.fields import RichTextField

class Page(models.Model):
    title = models.CharField(verbose_name="Título", max_length=200)
    content = RichTextField(verbose_name="Contenido")
    order = models.SmallIntegerField(verbose_name="Orden", default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "página"
        verbose_name_plural = "páginas"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Company_number(models.Model):
    ondernemin = models.CharField(verbose_name="ondernemin", max_length=150)
    vestiging = models.CharField(verbose_name="vestiging", max_length=150)
    ovamnum = models.CharField(verbose_name="ovamnum", max_length=150)
    ovamvolg = models.CharField(verbose_name="ovamvolg", max_length=150)
    naam = models.CharField(verbose_name="naam", max_length=150)
    straat = models.CharField(verbose_name="straat", max_length=150)
    adresuitbreiding = models.CharField(verbose_name="adresuitbreiding", max_length=150)
    huisnummer = models.CharField(verbose_name="huisnummer", max_length=150)
    postcode = models.CharField(verbose_name="postcode", max_length=150)
    gemeente = models.CharField(verbose_name="gemeente", max_length=150)
    landcode = models.CharField(verbose_name="landcode", max_length=150)
    cbb = models.CharField(verbose_name="cbb", max_length=150)

    class Meta:
        ordering = ['id']
    