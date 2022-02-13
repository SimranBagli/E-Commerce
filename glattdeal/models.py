from django.db import models
from django.contrib.auth.models import  User
from django.utils.timezone import now

# Create your models here.
class Category(models.Model):
    cat_title=models.CharField(max_length=200)
    cat_image= models.ImageField(upload_to='images/cat_images', null=True, blank=True, help_text="Upload only .png and.jpg")

    def __str__(self):
        return self.cat_title

class Location(models.Model):
    location_name=models.CharField(max_length=200)
    def __str__(self):
        return self.location_name

class Supplier(models.Model):
    supplier_name=models.CharField(max_length=200)
    supplier_email=models.CharField(max_length=200)
    supplier_password=models.CharField(max_length=200)
    supplier_username=models.CharField(max_length=200)
    supplier_address=models.CharField(max_length=200)
    supplier_contact=models.CharField(max_length=50)
    supplier_details=models.CharField(max_length=1500,null=True)
    supplier_image1 = models.ImageField(upload_to='images/supp_images', null=True, blank=True, help_text="Upload only .png and jpg")
    supplier_image2 = models.ImageField(upload_to='images/supp_images', null=True, blank=True, help_text="Upload only .png and jpg")
    supplier_image3 = models.ImageField(upload_to='images/supp_images', null=True, blank=True, help_text="Upload only .png and jpg")
    userid= models.ForeignKey(User, on_delete=models.CASCADE)
    supplier_starttime=models.CharField(max_length=10,null=True)
    supplier_endtime=models.CharField(max_length=10,null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE, null=True,blank=True)
    def __str__(self):
        return self.supplier_name

class Deal(models.Model):
    deal_title=models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    deal_desc=models.CharField(max_length=1500,null=True)
    deal_actualprice=models.IntegerField(blank=True,default=0)
    deal_discount=models.IntegerField(blank=True,default=0)
    deal_price=models.IntegerField(blank=True,default=0)
    deal_postedon=models.DateTimeField(default=now)
    deal_startdate=models.DateTimeField(blank=True,null=True)
    deal_enddate=models.DateTimeField(blank=True,null=True)
    deal_postedby= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.deal_title

class UserDetail(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    user_info = models.CharField(max_length=500, null=True, blank=True)
    user_fname = models.CharField(max_length=100, null=True, blank=True)
    user_lname = models.CharField(max_length=100, null=True, blank=True)
    user_image = models.ImageField(upload_to='images/user_images', null=True, blank=True,
                                   help_text="Upload only .png and jpg")
    user_city = models.CharField(max_length=100, null=True, blank=True)
    user_phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.user)

class UserDetail(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __unicode__(self):
        return  User

class Cart(models.Model):
    deal_id = models.ForeignKey(Deal, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price=models.IntegerField(blank=True,default=0)
    quantity=models.IntegerField(blank=True,default=0)
    total=models.IntegerField(blank=True,default=0)

    def __str__(self):
        return str(self.deal_id)

class Payment(models.Model):
    deal_id= models.CharField(max_length=100, null=True)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING,null=True,blank=True)
    total_amount=models.IntegerField(blank=True,default=0)
    item_amount=models.IntegerField(blank=True,default=0)
    quantity=models.IntegerField(blank=True,default=0)
    payment_amount=models.IntegerField(blank=True,default=0)
    #payment_date=models.DateTimeField(default=datetime.now)
    payment_date=models.DateTimeField(default=now,null=True)
    txn_id = models.CharField(max_length=100, null=True)
    payment_currency = models.CharField(max_length=10, null=True)
    payment_status = models.CharField(max_length=10, null=True)
    payer_email = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.deal_id)


class Reviews(models.Model):
    deal_id= models.ForeignKey(Deal, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rate=models.IntegerField(blank=True,default=0)
    review_on=models.DateTimeField(default=now)
    subject = models.CharField(max_length=100, null=True)
    review = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.review



