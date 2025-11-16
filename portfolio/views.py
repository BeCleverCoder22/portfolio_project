from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from datetime import timedelta
import json
from .models import Project, Skill, Experience, Contact, SiteVisit, SiteSettings
from .forms import ContactForm, ProjectFilterForm

def get_client_ip(request):
    """Récupère l'adresse IP réelle du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_site_settings():
    return SiteSettings.objects.first()

def home(request):
    settings = get_site_settings()
    featured_projects = Project.objects.filter(featured=True, status='completed')[:3]
    skills = Skill.objects.all()
    
    context = {
        'settings': settings,
        'featured_projects': featured_projects,
        'skills': skills,
    }
    return render(request, 'portfolio/home.html', context)

def projects(request):
    settings = get_site_settings()
    
    projects_list = Project.objects.filter(
        Q(status='completed') | Q(status='in_progress')
    ).prefetch_related('technologies')
    
    # Filtres simples via GET parameters
    tech_filter = request.GET.get('tech')
    status_filter = request.GET.get('status')
    search_query = request.GET.get('search')
    
    if tech_filter:
        # Filtrer par technologie (en utilisant le nom de la skill)
        projects_list = projects_list.filter(technologies__name__icontains=tech_filter)
    
    if status_filter:
        projects_list = projects_list.filter(status=status_filter)
    
    if search_query:
        projects_list = projects_list.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(detailed_description__icontains=search_query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(projects_list, 6)  # 6 projets par page
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    # Statistiques
    total_projects = Project.objects.count()
    completed_projects = Project.objects.filter(status='completed').count()
    technologies = Skill.objects.all()
    
    context = {
        'settings': settings,
        'projects': projects,
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'technologies': technologies,
        'current_tech': tech_filter,
        'current_status': status_filter,
        'current_search': search_query,
    }
    return render(request, 'portfolio/projects.html', context)

def project_detail(request, slug):
    settings = get_site_settings()
    project = get_object_or_404(Project, slug=slug)
    project.increment_views()
    
    related_projects = Project.objects.filter(
        technologies__in=project.technologies.all()
    ).exclude(id=project.id).distinct()[:3]
    
    context = {
        'settings': settings,
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'portfolio/project_detail.html', context)

def about(request):
    settings = get_site_settings()
    experiences = Experience.objects.all()
    skills = Skill.objects.all()
    total_projects = Project.objects.count()
    
    context = {
        'settings': settings,
        'experiences': experiences,
        'skills': skills,
        'total_projects': total_projects,
    }
    return render(request, 'portfolio/about.html', context)

def contact(request):
    settings = get_site_settings()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            # Ajouter les informations de tracking
            contact_message.ip_address = get_client_ip(request)
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            contact_message.save()
            
            messages.success(
                request, 
                'Votre message a été envoyé avec succès! Nous vous répondrons dans les plus brefs délais.'
            )
            return redirect('contact')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = ContactForm()
    
    context = {
        'settings': settings,
        'form': form,
    }
    return render(request, 'portfolio/contact.html', context)

@login_required
def dashboard(request):
    # Statistiques générales
    total_projects = Project.objects.count()
    total_messages = Contact.objects.count()
    unread_messages = Contact.objects.filter(read=False).count()
    
    # Statistiques de trafic
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    visits_today = SiteVisit.objects.filter(timestamp__date=today).count()
    visits_week = SiteVisit.objects.filter(timestamp__date__gte=week_ago).count()
    visits_month = SiteVisit.objects.filter(timestamp__date__gte=month_ago).count()
    
    # Projets les plus vus
    top_projects = Project.objects.order_by('-views')[:5]
    
    # Messages récents
    recent_messages = Contact.objects.order_by('-created_at')[:5]
    
    # Pages les plus visitées
    popular_pages = SiteVisit.objects.values('page').annotate(
        count=Count('page')
    ).order_by('-count')[:5]
    
    context = {
        'total_projects': total_projects,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'visits_today': visits_today,
        'visits_week': visits_week,
        'visits_month': visits_month,
        'top_projects': top_projects,
        'recent_messages': recent_messages,
        'popular_pages': popular_pages,
    }
    
    return render(request, 'admin/dashboard.html', context)

# API Views pour les statistiques en temps réel
@login_required
def api_stats(request):
    """API pour récupérer les statistiques en temps réel"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    stats = {
        'visits_today': SiteVisit.objects.filter(timestamp__date=today).count(),
        'visits_week': SiteVisit.objects.filter(timestamp__date__gte=week_ago).count(),
        'unread_messages': Contact.objects.filter(read=False).count(),
        'total_projects': Project.objects.count(),
    }
    
    return JsonResponse(stats)

@login_required
def api_chart_data(request):
    """API pour les données de graphiques"""
    days = 7
    dates = []
    visits = []
    
    for i in range(days):
        date = (timezone.now().date() - timedelta(days=i))
        dates.append(date.strftime('%d/%m'))
        visit_count = SiteVisit.objects.filter(timestamp__date=date).count()
        visits.append(visit_count)
    
    return JsonResponse({
        'labels': list(reversed(dates)),
        'data': list(reversed(visits))
    })

def download_cv(request):
    """Télécharger le CV"""
    settings = get_site_settings()
    if settings and settings.resume_file:
        response = HttpResponse(settings.resume_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="CV_{settings.name.replace(" ", "_")}.pdf"'
        return response
    else:
        messages.error(request, 'CV non disponible')
        return redirect('home')

# Vue pour marquer un message comme lu (AJAX)
@login_required
def mark_message_read(request, message_id):
    if request.method == 'POST':
        try:
            message = Contact.objects.get(id=message_id)
            message.mark_as_read()
            return JsonResponse({'success': True})
        except Contact.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message non trouvé'})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

# Vue cache pour la page d'accueil (amélioration des performances)
@cache_page(60 * 15)  # Cache pendant 15 minutes
def cached_home(request):
    return home(request)