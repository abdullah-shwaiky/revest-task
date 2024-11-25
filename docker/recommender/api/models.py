from django.db import models

# Create your models here.
class Products(models.Model):
    product_id = models.TextField(primary_key=True)
    category = models.TextField(blank=True, null=True)
    sub_category = models.TextField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'