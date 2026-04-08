from django import forms
from .models import Airport, Route


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['from_airport', 'to_airport', 'position', 'duration']

    def clean(self):
        cleaned_data = super().clean()
        from_airport = cleaned_data.get('from_airport')
        to_airport = cleaned_data.get('to_airport')

        if from_airport == to_airport:
            raise forms.ValidationError(
                "Source and destination cannot be same.")

        return cleaned_data


class NthNodeForm(forms.Form):
    start_airport = forms.CharField(max_length=10)
    direction = forms.ChoiceField(
        choices=[('left', 'Left'), ('right', 'Right')]
    )
    steps = forms.IntegerField(min_value=1)

    def clean_start_airport(self):
        code = self.cleaned_data['start_airport'].upper()

        if not Airport.objects.filter(code=code).exists():
            raise forms.ValidationError("Airport does not exist.")

        return code


class ShortestPathForm(forms.Form):
    source = forms.CharField(max_length=10)
    destination = forms.CharField(max_length=10)

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        destination = cleaned_data.get('destination')

        if source == destination:
            raise forms.ValidationError(
                "Source and destination cannot be same.")

        return cleaned_data

    def clean_source(self):
        code = self.cleaned_data['source'].upper()
        if not Airport.objects.filter(code=code).exists():
            raise forms.ValidationError("Invalid source airport")
        return code

    def clean_destination(self):
        code = self.cleaned_data['destination'].upper()
        if not Airport.objects.filter(code=code).exists():
            raise forms.ValidationError("Invalid destination airport")
        return code
