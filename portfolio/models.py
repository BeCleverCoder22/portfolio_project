from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
import os

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('tools', 'Outils & Autres'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Catégorie")
    proficiency = models.IntegerField(default=50, verbose_name="Niveau (%)", 
                                     help_text="0-100")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icône CSS")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        ordering = ['category', 'order']
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Terminé'),
        ('in_progress', 'En cours'),
        ('archived', 'Archivé'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description courte")
    detailed_description = RichTextField(verbose_name="Description détaillée")
    image = models.ImageField(upload_to='projects/', verbose_name="Image principale")
    technologies = models.ManyToManyField(Skill, verbose_name="Technologies utilisées")
    github_url = models.URLField(blank=True, verbose_name="Lien GitHub")
    demo_url = models.URLField(blank=True, verbose_name="Lien démo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                            default='completed', verbose_name="Statut")
    featured = models.BooleanField(default=False, verbose_name="Projet mis en avant")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    views = models.IntegerField(default=0, verbose_name="Nombre de vues")
    
    class Meta:
        ordering = ['-featured', 'order', '-created_at']
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class Experience(models.Model):
    company = models.CharField(max_length=200, verbose_name="Entreprise")
    position = models.CharField(max_length=200, verbose_name="Poste")
    description = RichTextField(verbose_name="Description")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    current = models.BooleanField(default=False, verbose_name="Poste actuel")
    location = models.CharField(max_length=200, blank=True, verbose_name="Lieu")
    order = models.IntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        ordering = ['-start_date', 'order']
        verbose_name = "Expérience"
        verbose_name_plural = "Expériences"
    
    def __str__(self):
        return f"{self.position} chez {self.company}"

class Contact(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    company = models.CharField(max_length=200, blank=True, verbose_name="Entreprise")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Priorité")
    project_budget = models.CharField(max_length=100, blank=True, verbose_name="Budget estimé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    read = models.BooleanField(default=False, verbose_name="Lu")
    replied = models.BooleanField(default=False, verbose_name="Répondu")
    reply_message = models.TextField(blank=True, verbose_name="Message de réponse")
    replied_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de réponse")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Adresse IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    
    def __str__(self):
        return f"Message de {self.name} - {self.subject}"
    
    def mark_as_read(self):
        self.read = True
        self.save(update_fields=['read'])
    
    def get_priority_badge_class(self):
        priority_classes = {
            'low': 'bg-success',
            'medium': 'bg-info',
            'high': 'bg-warning',
            'urgent': 'bg-danger',
        }
        return priority_classes.get(self.priority, 'bg-secondary')

# Signal pour envoyer un email lors de la création d'un nouveau message
@receiver(post_save, sender=Contact)
def send_new_message_notification(sender, instance, created, **kwargs):
    if created:  # Seulement pour les nouveaux messages
        try:
            # Email à l'administrateur
            admin_subject = f'Nouveau message - {instance.subject}'
            admin_message = f'''
Nouveau message reçu sur votre portfolio :

Nom: {instance.name}
Email: {instance.email}
Téléphone: {instance.phone or 'Non renseigné'}
Entreprise: {instance.company or 'Non renseignée'}
Sujet: {instance.subject}
Priorité: {instance.get_priority_display()}
Budget: {instance.project_budget or 'Non renseigné'}

Message:
{instance.message}

---
Envoyé le: {instance.created_at.strftime('%d/%m/%Y à %H:%M')}
IP: {instance.ip_address or 'Non disponible'}
            '''
            
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=True,
            )
            
            # Email de confirmation à l'expéditeur
            user_subject = f'Confirmation de réception - {instance.subject}'
            user_message = f'''
Bonjour {instance.name},

Nous avons bien reçu votre message concernant "{instance.subject}".

Votre message:
{instance.message}

Nous vous répondrons dans les plus brefs délais.

Cordialement,
Ulrich AMOUZOU-ABLO
            '''
            
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=True,
            )
            
        except Exception as e:
            # Log l'erreur mais ne fait pas échouer la création du message
            print(f'Erreur envoi email: {e}')

class SiteVisit(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="Adresse IP")
    user_agent = models.TextField(verbose_name="User Agent")
    page = models.CharField(max_length=500, verbose_name="Page visitée")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date/Heure")
    session_key = models.CharField(max_length=100, blank=True, verbose_name="Session")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Visite"
        verbose_name_plural = "Visites"
    
    def __str__(self):
        return f"{self.ip_address} - {self.page} - {self.timestamp}"

class SiteSettings(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom complet")
    tagline = models.CharField(max_length=300, verbose_name="Slogan/Tagline")
    bio = RichTextField(verbose_name="Biographie")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    location = models.CharField(max_length=200, verbose_name="Localisation")
    github = models.URLField(blank=True, verbose_name="GitHub")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp", help_text="Numéro de téléphone au format international (ex: +33612345678)")
    resume_file = models.FileField(upload_to='resumes/', blank=True, verbose_name="CV (PDF)")
    profile_image = models.ImageField(upload_to='profile/', blank=True, verbose_name="Photo de profil")
    
    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"
    
    def __str__(self):
        return "Paramètres du Portfolio"
    
    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Il ne peut y avoir qu'une seule instance de SiteSettings")
        return super().save(*args, **kwargs)