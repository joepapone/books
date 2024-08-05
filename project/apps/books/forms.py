from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Rating validation function 
def validate_rating(value):
    if not 0 <= value <= 5:
        raise ValidationError(
            _("%(value)s Requires a number between 0 and 5"),
            params={"value": value},
        )


class RatingForm(forms.Form):
    id = forms.IntegerField()
    stars = forms.IntegerField(validators=[validate_rating])
    next = forms.CharField()


    """
    # Function for validating
    def clean(self):
        # data from the form is fetched using super function
        super(RatingForm, self).clean()
         
        # Extract field data
        stars = self.cleaned_data.get('stars')
 
        # Validation conditions
        if not 1 <= stars <= 5:
            self._errors['stars'] = self.error_class([
                _("%(stars)s requires a number between 1 and 5")])
 
        # return any errors if found
        return self.cleaned_data
    """