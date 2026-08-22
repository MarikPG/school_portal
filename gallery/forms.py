from django import forms

from .models import MediaItem


class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = [
            'title',
            'description',
            'file',
            'media_type',
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Назва файлу',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Опис...',
                }
            ),

            'file': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'media_type': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
        }