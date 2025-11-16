from .models import SiteVisit

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Tracker uniquement les pages non-admin
        if not request.path.startswith('/admin/'):
            try:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                
                SiteVisit.objects.create(
                    ip_address=ip,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                    page=request.path,
                    session_key=request.session.session_key or ''
                )
            except:
                pass
        
        return response