from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.mail import send_mail



class HomeView(TemplateView):
    def get_template_names(self):
        if 'zarathustratech.com' in self.request.get_host():
            return 'home_company.html'
        return 'home_app.html'


class AppView(TemplateView):
    template_name = 'app.html'

    def dispatch(self, request, *args, **kwargs):
        if 'zarathustratech.com' in request.get_host():
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class ContactView(RedirectView):
    def get_redirect_url(self):
        try:
            send_mail(
                'New message',
                str(self.request.POST),
                'info@zarathustratech.com',
                ['info@zarathustratech.com'],
                fail_silently=False,
            )
            messages.success(self.request, 'Message sent.')
        except:
            msg = 'We could not receiv your message. Please try sending' \
                  'an email to info@zarathustratech.com'
            messages.error(self.request, msg)
        return '/'
