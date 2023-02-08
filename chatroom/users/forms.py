from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


User = get_user_model()




class AuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class':"textinput textInput form-control",
            'type':"text", 
            'name':"username", 
            'maxlength':"150", 
            'placeholder':"Введите логин",  
            'id':"id_username"})

        self.fields['password'].widget.attrs.update({
            'class':"textinput textInput form-control",
            'type':"password", 
            'name':"password", 
            "autocomplete":"current-password",
            'placeholder':"Введите пароль",  
            'id':"id_password"})
        
     
class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class':"textinput textInput form-control",
            'type':"text", 
            'name':"username", 
            'maxlength':"150", 
            'placeholder':"Введите логин",  
            'id':"id_username"})

        self.fields['password1'].widget.attrs.update({
            'class':"textinput textInput form-control",
            'type':"password", 
            'name':"password1", 
            "autocomplete":"new-password",
            'placeholder':"Введите пароль",  
            'id':"id_password1"})

        self.fields['password2'].widget.attrs.update({
            'class':"textinput textInput form-control",
            'type':"password", 
            'name':"password2", 
            "autocomplete":"new-password",
            'placeholder':"Подтвердите пароль",  
            'id':"id_password1"})


    class Meta(UserCreationForm.Meta):
        model = User



