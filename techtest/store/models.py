from django.db import models

# Create your models here.

class ProductDetails(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(null=False, max_length=100)
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __unicode__(self):
        return unicode(self.product_id)

    def save(self, *args, **kwargs):
        super(ProductDetails, self).save(*args, **kwargs)



class ProductCart(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(null=False, max_length=100)
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    qty = models.IntegerField(default=1)
    
    def __unicode__(self):
        return unicode(self.product_id)

    def save(self, *args, **kwargs):
        super(ProductCart, self).save(*args, **kwargs)