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

class GoalType(models.Model):
    goal_objective = models.CharField(max_length=300, blank=True)
    goal_choice = (
            ('Savings', 'Savings'),
            ('Expenses', 'Expenses'), 
            ('Debt', 'Debt')
    )
    goal_choice_type = models.CharField(max_length = 30, blank=True, null=True, choices=goal_choice)
    goal_accomplished = models.BooleanField()

    def _unicode_(self):
        return self.goal_objective

