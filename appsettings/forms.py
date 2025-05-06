from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['profile_picture']
    
    
    # Optional: You can include validation for file size or file type here
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and picture.size > 5 * 1024 * 1024:  # 5MB max
            raise forms.ValidationError("File size is too large. Max allowed is 5MB.")
        return picture