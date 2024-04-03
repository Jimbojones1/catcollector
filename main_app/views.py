from django.shortcuts import render


# Add this cats list below the imports
cats = [
  {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
  {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
]
# Create your views here.
def home(request):

	return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')


def cats_index(request):
	return render(request, 'cats/index.html', {
		'cats': cats
		#'cats' becomes a variable name in 'cats/index.html'
		# just like express 
		# res.render('cats/index', {'cats': cats})
	})