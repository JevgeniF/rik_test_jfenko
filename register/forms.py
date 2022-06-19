from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import Osayhing, Isik, JurIsik


# The OsayhingForm class inherits from the ModelForm class, and it's used to create a form based on the Osayhing model.
class OsayhingForm(ModelForm):
    # > The `Meta` class is a special class that allows us to set extra options on our model
    class Meta:
        model = Osayhing
        fields = (
            'nimi',
            'registrikood',
            'asutamiskuup',
            'kogukapital'
        )
        labels = {
            'nimi': 'Osaühingu Nimi',
            'registrikood': 'Registrikood',
            'asutamiskuup': 'Asutamiskuupäev',
            'kogukapital': 'Kogukapital (EUR)'
        }
        widgets = {
            'nimi': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                           'placeholder': 'min 3 max 100 märgi', 'minlength': 3,
                                           'maxlength': 100}),
            'registrikood': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': '7 numbrit',
                                                   'minlength': 7, 'maxlength': 7}),
            'asutamiskuup': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'kogukapital': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control',
                                                    'placeholder': 'min 2500', 'min': 2500}),
        }


# The JurIsikForm class inherits from the ModelForm class, and it's used to create a form based on the JurIsik model.
class JurIsikForm(ModelForm):
    class Meta:
        model = JurIsik
        fields = (
            'nimi',
            'kood',
            'j_osaniku_osa'
        )
        labels = {
            'nimi': 'Jur. Isiku Nimi',
            'kood': 'Registrikood',
            'j_osaniku_osa': 'Osaniku osa (EUR)'
        }
        widgets = {
            'nimi': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                           'placeholder': 'minlength 3 max 100 märgi', 'minlength': 3,
                                           'maxlength': 100}),
            'kood': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': '7 numbrit',
                       'minlength': 7, 'maxlength': 7}),
            'j_osaniku_osa': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control',
                                                      'placeholder': 'min 1 EUR', 'min': 1}),
        }


# The IsikForm class inherits from the ModelForm class, and it's used to create a form based on the Isik model.
class IsikForm(ModelForm):
    class Meta:
        model = Isik
        fields = (
            'eesnimi',
            'perenimi',
            'isikukood',
            'f_osaniku_osa'
        )
        labels = {
            'eesnimi': 'Eesnimi',
            'perenimi': 'Perenimi',
            'isikukood': 'Isikukood',
            'f_osaniku_osa': 'Osaniku osa (EUR)'
        }
        widgets = {
            'eesnimi': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                              'placeholder': 'minlength 3 max 100 märgi', 'minlength': 3,
                                              'maxlength': 100}),
            'perenimi': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                               'placeholder': 'minlength 3 max 100 märgi', 'minlength': 3,
                                               'maxlength': 100}),
            'isikukood': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': '11 numbrit',
                                                'minlength': 11, 'maxlength': 11}),
            'f_osaniku_osa': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control',
                                                      'placeholder': 'min 1 EUR', 'min': 1}),
        }


# The JurIsikFormSet for generation of some amount of JurIsik model forms.
JurIsikFormSet = modelformset_factory(
    JurIsik,  # model
    extra=5,    # amount of forms to generate
    fields=(
        'nimi',
        'kood',
        'j_osaniku_osa'
    ),
    labels={
        'nimi': 'Jur. Isiku Nimi',
        'kood': 'Registrikood',
        'j_osaniku_osa': 'Osaniku osa (EUR)'
    },
    widgets={
        'nimi': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                       'placeholder': 'minlength 3 max 100 märgi', 'minlength': 3,
                                       'maxlength': 100}),
        'kood': forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': '7 numbrit',
                   'minlength': 7, 'maxlength': 7}),
        'j_osaniku_osa': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control',
                                                  'placeholder': 'min 1 EUR', 'min': 1}),
    }
)

# The IsikFormSet for generation of some amount of Isik model forms.
IsikFormSet = modelformset_factory(
    Isik,   # model
    extra=5,    # amount of forms to generate
    fields=(
        'eesnimi',
        'perenimi',
        'isikukood',
        'f_osaniku_osa'
    ),
    labels={
        'eesnimi': 'Eesnimi',
        'perenimi': 'Perenimi',
        'isikukood': 'Isikukood',
        'f_osaniku_osa': 'Osaniku osa (EUR)'
    },
    widgets={
        'eesnimi': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                          'placeholder': 'minlength 3 max 100 märgi', 'minlength': 3,
                                          'maxlength': 100}),
        'perenimi': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                           'placeholder': 'minlength 3 max 100 märgi', 'minlength': 3,
                                           'maxlength': 100}),
        'isikukood': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': '11 numbrit',
                                            'minlength': 11, 'maxlength': 11}),
        'f_osaniku_osa': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control',
                                                  'placeholder': 'min 1 EUR', 'min': 1}),
    }
)
