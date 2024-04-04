from django.db import models
from django.urls import reverse

# Create your models here.


class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    # this can handle create, update actions
    def get_absolute_url(self):
        # 'detail is refering to the name of the url we want to redirect to'
        # path('cats/<int:cat_id>/', views.cats_detail, name='detail'),
        return reverse('detail', kwargs={'cat_id': self.id})
                                # cat_id refers to the name of the param
                                # refer to the route above, and the value, 
                                # self.id, refers to the cat that was just created
                                # on the post request