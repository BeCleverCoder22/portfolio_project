from django import forms
from .models import Contact, Project

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'company', 'subject', 'message', 'priority', 'project_budget']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@exemple.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre numéro de téléphone'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de votre entreprise (optionnel)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sujet de votre message',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Décrivez votre projet ou votre demande en détail...',
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'project_budget': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Budget estimé (optionnel)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes Bootstrap et des labels personnalisés
        self.fields['name'].label = "Nom complet *"
        self.fields['email'].label = "Adresse email *"
        self.fields['phone'].label = "Téléphone"
        self.fields['company'].label = "Entreprise"
        self.fields['subject'].label = "Sujet *"
        self.fields['message'].label = "Message *"
        self.fields['priority'].label = "Priorité"
        self.fields['project_budget'].label = "Budget estimé"
        
        # Définir l'ordre des champs
        self.field_order = ['name', 'email', 'phone', 'company', 'subject', 'priority', 'project_budget', 'message']

class ProjectFilterForm(forms.Form):
    TECHNOLOGY_CHOICES = [('', 'Toutes les technologies')]
    STATUS_CHOICES = [('', 'Tous les statuts'), ('completed', 'Terminé'), ('in_progress', 'En cours')]
    
    technology = forms.ChoiceField(choices=TECHNOLOGY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Rechercher un projet...'
    }))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Charger dynamiquement les technologies
        from .models import Skill
        tech_choices = [('', 'Toutes les technologies')]
        tech_choices.extend([(skill.name, skill.name) for skill in Skill.objects.all()])
        self.fields['technology'].choices = tech_choices