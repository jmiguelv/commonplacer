from django.forms import ModelForm
from models import Classroom


class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
