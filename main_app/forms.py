
from django.forms import ModelForm
from .models import Feeding

class FeedingForm(ModelForm):
	class Meta:
		# meta class is configuration options for a class
		# this is straight from the docs
		model = Feeding
		fields = ['date', 'meal']