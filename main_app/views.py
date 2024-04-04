from django.shortcuts import render

from django.views.generic.edit import CreateView
# from the ./models import Cat
from .models import Cat

# Add this cats list below the imports
# Create your views here.
def home(request):
	cats = Cat.objects.all()

	return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')



class CatCreate(CreateView):
	model = Cat 
	fields = '__all__'


def cats_index(request):

	# tell the model to find all the rows in the cats table!
	cats = Cat.objects.all()
	return render(request, 'cats/index.html', {
		'cats': cats
		# 'cats' becomes a variable name in 'cats/index.html'
		# just like express
		# res.render('cats/index', {'cats': cats})
	})

# cat_id comes from the path in the urls.py 
# path('cats/<int:cat_id>/', views.cats_detail, name='detail'),
def cats_detail(request, cat_id):
	# tell the model to find the row that matches cat_id from the request in the database
	cat = Cat.objects.get(id=cat_id)
	return render(request, 'cats/detail.html', {
		'cat': cat
		# 'cat is the variable name in cats/detail.html 
	})
