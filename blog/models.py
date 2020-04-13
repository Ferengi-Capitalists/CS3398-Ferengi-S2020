from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

class Goal(models.Model): 
	title = models.CharField(max_length= 10000)
	content = models.TextField(blank=True, null=True)
	amount = models.DecimalField(decimal_places=2, max_digits = 12)
	date_posted = models.DateTimeField(default= timezone.now)
	completed = models.BooleanField()