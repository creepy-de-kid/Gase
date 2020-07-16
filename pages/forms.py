from django import forms

class Contactform(forms.Form):
  fullname_atrrs = {
    'class': 'form-control',
    'id': 'fullname',
    'placeholder': 'Fullname',
    'maxlenth': '100'
  }
  email_atrrs = {
    'class': 'form-control',
    'id': 'email',
    'placeholder': 'Email',
  }
  content_atrrs = {
    'class': 'form-control',
    'id': 'content',
    'cols': '30',
    'rows': '10',
    'placeholder': 'Message',
  }

  fullname = forms.CharField(widget=forms.TextInput(attrs=fullname_atrrs))
  email = forms.EmailField(widget=forms.EmailInput(attrs=email_atrrs))
  content = forms.CharField(widget=forms.Textarea(attrs=content_atrrs))

  def clean_email(self):
    email = self.cleaned_data.get('email')

    if not 'gmail.com' or 'yahoo.com':
      raise forms.ValidationError("Email has to be gmail or yahoo mail.")
    
    return email