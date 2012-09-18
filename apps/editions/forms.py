from django.forms import ModelForm, Textarea
from models import Classroom


class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        exclude = ['leader']
        widgets = {'description': Textarea(attrs={'cols': 80, 'rows': 2}), }
