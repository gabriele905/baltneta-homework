from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    category = models.CharField(max_length=255)
    number = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.category
