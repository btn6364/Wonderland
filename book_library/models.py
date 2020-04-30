from django.db import models
from PIL import Image
from django.utils import timezone

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    about = models.TextField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    pages = models.IntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(default="default_book.jpg", upload_to="book_pic")
    source = models.URLField(max_length=250)
    published_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # TODO add rating here

    def __str__(self):
        return self.title + "-" + self.author.first_name + " " + self.author.last_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # resize the image
        img = Image.open(self.image.path)
        if img.height > 400 or img.width > 600:
            output_size = (400, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

