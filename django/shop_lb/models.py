from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError
from django.db.models import Model
from django.db import models

class Category(Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.name

class Getter(Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.name

class Product(Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name="Фото товара")
    price = models.DecimalField(
        max_length=10, 
        decimal_places=2, 
        max_digits=10, 
        validators=[MinValueValidator(0)],
        verbose_name="Цена"
    )
    stock_quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Количество на складе"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    manufacturer = models.ForeignKey(Getter, on_delete=models.CASCADE, verbose_name="Производитель")

    def __str__(self):
        return self.name

class Bucket(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def total_price(self):
        return sum(item.item_price() for item in self.items.all())
    
    total_price.short_description = "Общая стоимость"

class Bucket_Element(Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, verbose_name="Корзина пользователя")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    number = models.PositiveIntegerField(verbose_name="Kоличество единиц товара в корзине")

    def __str__(self):
        return f"{self.product.name}({self.number}.шт)"
    def cost(self):
        return self.number * self.product.price
    
    def clean(self):
        if self.product and self.number > self.product.stock_quantity:
            raise ValidationError({
                'number': f"Недостаточно товара на складе. Доступно: {self.product.stock_quantity}"
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)