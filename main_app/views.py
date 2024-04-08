from django.shortcuts import render, redirect, HttpResponse

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

# stuff for photo upload for aws
import uuid # for random numbers (used in generating photo name)
import boto3 # aws sdk that lets us talk to our s3 bucket
import os # this lets us talk to the .env

# from the ./models import Cat
from .models import Cat, Toy, Photo

from .forms import FeedingForm
# Add this cats list below the imports
# Create your views here.
def home(request):
	cats = Cat.objects.all()

	return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')

# path('cats/<int:cat_id>/add_photo/', cat_id comes from the param
def add_photo(request, cat_id):
	# photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = 'catcollector/' + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, cat_id=cat_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', cat_id=cat_id)




def disassoc_toy(request, cat_id, toy_id):
	cat = Cat.objects.get(id=cat_id)
	cat.toys.remove(toy_id)
	return redirect('detail',cat_id=cat_id)

# cats/<int:cat_id>/assoc_toy/<int:toy_id>/
def assoc_toy(request, cat_id, toy_id):
	print(cat_id, toy_id )
	cat = Cat.objects.get(id=cat_id)
	cat.toys.add(toy_id)# adding a row to our through table the one with 2 foriegn keys in sql
	return redirect('detail', cat_id=cat_id)
# CatCreate reuses the same template as the CatUpdate
# <your app>/<model_name>_form.html
# ex. templates/main_app/cat_form.html
# handle get requests to cat/create
# handles post requests to cat/create
class CatCreate(CreateView):
	model = Cat 
	fields = ['name', 'breed', 'description', 'age']

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

	# We want to search for all the toys that cat does not have!

	# 1. create a list of ids of the toys the cat does have!
	id_list = cat.toys.all().values_list('id')
	# Now we can query the toys table for a the toys 
	# that are not in the id_list!     field looksup in django (google this)
	toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)


	# instatiate the feeding form class to create an instance of the class
	# in otherwords a form object
	feeding_form = FeedingForm()
	print(cat.__dict__)
	return render(request, 'cats/detail.html', {
		'cat': cat,
		'feeding_form': feeding_form,
		'toys': toys_cat_doesnt_have
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


class ToyList(ListView):
    model = Toy


class ToyDetail(DetailView):
    model = Toy


class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'


class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']


class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'