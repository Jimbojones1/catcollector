from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

# you can access the cat with cat_set when you have toy
class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})










class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # add a Many to Many field
    toys = models.ManyToManyField(Toy)
    # 1 user has many cats
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # this can handle create, update actions
    def get_absolute_url(self):
        # 'detail is refering to the name of the url we want to redirect to'
        # path('cats/<int:cat_id>/', views.cats_detail, name='detail'),
        return reverse("detail", kwargs={"cat_id": self.id})
        # cat_id refers to the name of the param
        # refer to the route above, and the value,
        # self.id, refers to the cat that was just created
        # on the post request


class Photo(models.Model):
    url = models.CharField(max_length=200)
    # cat_id, django automatically adds the _id to conform to psql conventions
    # 1 to many relationship
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Photo for cat_id: {self.cat_id} @{self.url}"



MEALS = (("B", "Breakfast"), ("L", "Lunch"), ("D", "Dinner"))


# One Cat has many Feedings, A feeding belongs to a cat
class Feeding(models.Model):
    date = models.DateField("feeding date")
    meal = models.CharField(
        max_length=1,
        # add the 'choices' field option
        choices=MEALS,
        # set the default value for meal to be 'B'
        default=MEALS[0][0],
    )

    # create a cat_id Foreign Key in psql
    # we don't put the id, django does automatically
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"
