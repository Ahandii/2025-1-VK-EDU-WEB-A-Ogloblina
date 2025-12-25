from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
from core.models import Profile 
from django.core.validators import FileExtensionValidator

def validate_image(img, max_upload_size):
    img_file = img.file
    
    if img_file.size > max_upload_size:
        size_mb = max_upload_size / (1024)
        err_msg = f'Размер файла не должен превышать {size_mb:.1f} KB'
        raise forms.ValidationError(err_msg)
    
    return img

class LoginForm(forms.Form):
    login = forms.CharField(label = "Login", max_length=255, required=True)
    password = forms.CharField(label = "Password", max_length=255, required=True, widget=forms.PasswordInput())

class SignupForm(forms.ModelForm):
    password = forms.CharField(label = "Password", max_length=255, required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label = "Repeat password", max_length=255, required=True, widget=forms.PasswordInput())
    avatar = forms.ImageField(label = "Upload avatar", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])], required=False)
    class Meta:
        model = User
        fields = [ "username", "email" ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password
    
    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        user_with_same_email_exists = User.objects\
            .exclude(id=self.instance.id)\
            .filter(email=email)\
            .exists()            
            
        if user_with_same_email_exists:
            raise forms.ValidationError({"email": "The user with same email exists"})

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError({"confirm_password": "Пароли не совпадают"})  
                                   
        return cleaned_data
    
    #def clean_avatar(self):
      #  avatar = self.cleaned_data.get('avatar')
      #  img = validate_image(avatar, 10 * 1024)
    #  return img 
    
    def save(self, commit=True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data.get('password'))
        
        if commit:
            user = super().save()
            profile = Profile.objects.create(user=user, avatar=self.cleaned_data['avatar'])
            profile.save()

        return user
    
class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label = "Avatar", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])], required=False)

    class Meta:
        model = User
        fields = [ "username", "email" ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email"
        self.fields["email"].required = True

        self.fields["username"].label = "Login"
        self.fields["username"].required = True
    
    def success_url(self):
        return reverse("core:settings")

    #def clean_avatar(self):
       # avatar = self.cleaned_data.get('avatar')
      #  img = validate_image(avatar, 10 * 1024)
     #   return img 
    
    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')

        user_with_same_email_exists = User.objects\
            .exclude(id=self.instance.id)\
            .filter(email=email)\
            .exists()            
            
        if user_with_same_email_exists:
            raise forms.ValidationError({"email": "The user with same email exists"})
                                           
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit = False)
        profile = Profile.objects.filter(user=user).first()
        if profile:
            if not profile.avatar:
                profile.avatar = self.cleaned_data['avatar']
        else:
            profile = Profile.objects.create(user=user, avatar=self.cleaned_data['avatar'])
        if commit:
            profile.save()
            super().save()
        return user