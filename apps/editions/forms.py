from django.forms import ModelForm, Textarea
from models import Classroom, Edition
from tinymce.widgets import TinyMCE


class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        exclude = ['leader']
        widgets = {'description': Textarea(attrs={'cols': 80,
            'rows': 2}), }


class EditionForm(ModelForm):
    class Meta:
        model = Edition
        exclude = ['author']
        fields = ['title', 'status', 'classroom', 'permission', 'tags',
                'text', 'comments']
        widgets = {'text': TinyMCE(attrs={'cols': 80, 'rows': 20}),
                'comments': Textarea(attrs={'cols': 80, 'rows': 2}), }
