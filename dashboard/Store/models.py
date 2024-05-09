from django.db import models
from django.contrib.auth.models import AbstractUser ,Group, Permission ,User
from django.core.validators import MinValueValidator

class Cust(AbstractUser):
    full_name = models.CharField(max_length=255)
    name_prefix = models.CharField(max_length=10, blank=True, null=True)
    middle_initial = models.CharField(max_length=1, blank=True, null=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    ssn = models.CharField(max_length=11)
    phone_no = models.CharField(max_length=20)
    place_name = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    region = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, related_name='custom_users')
    user = models.OneToOneField(User, related_name='custom_user', on_delete=models.CASCADE, primary_key=True)
    user_permissions = models.ManyToManyField(Permission, related_name='cust_users')
    image = models.ImageField(null = True, blank = True,upload_to = "images/")

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100 , primary_key=True)
    description = models.CharField(max_length=500,default='good category with good prices you can order it any time from our store have amazing ablities')
    
    def __str__(self):
        return self.name

class Item(models.Model):
    sku = models.CharField(max_length=100 , primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=1000,default='good item with good price you can order it any time from our store have amazing ablities')
    discAv = models.BooleanField(default= True)
    image = models.ImageField(null = True, blank = True,upload_to = "images/")
    Category = models.ForeignKey(Category, on_delete=models.CASCADE , default="Others")
    discAv = models.BooleanField(default= True)
    is_Active = models.BooleanField(default= True)

    def __str__(self):
        return self.sku

class order(models.Model):
    user = models.ForeignKey(Cust, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discout_percentage = models.DecimalField(default=0, max_digits=10, decimal_places=4,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    qty_ordered = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bill ID: {self.id}, User: {self.user.username}, Date: {self.order_date}"

class CustGroup(models.Model):
    cust = models.ForeignKey(Cust, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'store_cust_groups'
        managed = False

class ItemRate(models.Model):
    cust = models.ForeignKey(Cust, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rate = models.FloatField()

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    valid_from = models.DateField(blank=True, auto_now_add=True)
    valid_to = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class CouponUser(models.Model):
    user_id = models.ForeignKey(Cust, on_delete=models.CASCADE)
    Coupon_id = models.ForeignKey(Coupon, on_delete=models.CASCADE)
