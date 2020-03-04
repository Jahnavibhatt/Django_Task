from django.db import models
from django.contrib.auth.models import User
import ast

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, blank=True)
    phone_number = models.IntegerField(blank=True)


class MenuPdf(models.Model):
    pdf = models.FileField(upload_to='Menu/DELICIOUS_MENU.pdf')


class Menu(models.Model):
    # item_no = models.IntegerField(blank=True)
    item_name = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(blank=True)
    image = models.ImageField(null=True,upload_to="menu/")

class ListField(models.TextField):
    # __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return list(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Quntity = ListField()
    # item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    item = ListField()
    total = models.IntegerField(blank=True)
