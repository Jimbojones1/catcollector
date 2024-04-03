from django.shortcuts import render

# from the ./models import Cat
from .models import Cat

# Add this cats list below the imports
# Create your views here.
def home(request):

	return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')


def cats_index(request):
	# tell the model to find all the rows in the cats table!
	cats = Cat.objects.all()
	return render(request, 'cats/index.html', {
		'cats': cats
		#'cats' becomes a variable name in 'cats/index.html'
		# just like express 
		# res.render('cats/index', {'cats': cats})
	})

