from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from the ./models import Cat
from .models import Cat

from .forms import FeedingForm
# Add this cats list below the imports
# Create your views here.
def home(request):
	cats = Cat.objects.all()

	return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')

# CatCreate reuses the same template as the CatUpdate
# <your app>/<model_name>_form.html
# ex. templates/main_app/cat_form.html
# handle get requests to cat/create
# handles post requests to cat/create
class CatCreate(CreateView):
	model = Cat 
	fields = '__all__'

# CatUpdate reuses the same template as the CatCreate
# <your app>/<model_name>_form.html
# ex. templates/main_app/cat_form.html
class CatUpdate(UpdateView):
	model = Cat
	# disallow renaming of the cat
	fields = ['breed', 'description', 'age']
	# uses def get_absolute_url in models.py to redirect the put request
	# back to the the detail page of the cat just updated

class CatDelete(DeleteView):
	model = Cat 
	# define the success_url here because the def get_absolute_url in the models.property
	# redirects to a detail page which doesn't make sense since we deleted it
	success_url = '/cats' # redirect to cats_index path



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

	# instatiate the feeding form class to create an instance of the class
	# in otherwords a form object
	feeding_form = FeedingForm()
	return render(request, 'cats/detail.html', {
		'cat': cat,
		'feeding_form': feeding_form
		# 'cat is the variable name in cats/detail.html 
	})

# 'cats/<int:cat_id>/add_feeding/'
def add_feeding(request, cat_id):
	# process the form request form the client
	form = FeedingForm(request.POST)
	# request.POST is like req.body, its the contents of the form
	# validate the form
	if form.is_valid():
		# create an in memory instance (on django) of our data
		# to be added to psql, commit=False, don't save to db yet
		new_feeding = form.save(commit=False)
		# now we want to make sure we add the cat id to the new_feeding
		new_feeding.cat_id = cat_id
		new_feeding.save() # this is adding a feeding row to the feeding table in psql
	return redirect('detail', cat_id=cat_id) #cat_id is the name of the param in the url path, 
	# cat_id, is the id of the cat from the url request
