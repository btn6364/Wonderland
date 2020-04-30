from django.db import models
from PIL import Image
from django.utils import timezone
from utils.url_short import URL_Shortener

class Book(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    pages = models.IntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(default="default_book.jpg", upload_to="book_pic")
    source = models.URLField(max_length=300)
    published_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # TODO add rating here

    def __str__(self):
        return self.source

    def get_shorten_url(self):
        return URL_Shortener.shorten_url(self.__str__())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # resize the image
        img = Image.open(self.image.path)
        if img.height > 400 or img.width > 600:
            output_size = (400, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)
