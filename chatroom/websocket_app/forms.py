from django import forms
from .models import ChatRoom
from users.models import User

class CreateChatForm(forms.ModelForm):
    """Форма создания чата"""
    
    class Meta:
        model = ChatRoom
        fields = ['name']

    def __init__(self, *args, **kwargs):
        user= kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # исключение пользователя из выпадащего списка
        self.fields['users'] = forms.ModelMultipleChoiceField(queryset=User.objects.exclude(id=user.id))

