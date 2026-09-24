from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Home Page → /
    path('', views.index, name='home'),
   
    # Blog List Page → /blog/
    path('blog/', views.blog, name='blog'),

    # Blog Detail Page → /blog/details/
    path('blog/details/', views.blog_details, name='blog-details'),

    # Contact Page → /contact/
    path('contact/', views.contact, name='contact'),

    # Service Details Page → /service-details/
    path('service-details/', views.service_details, name='service-details'),

    # Contact Form Submission Endpoint
    path('contact-submit/', views.contact_submit, name='contact_submit'),

    # Newsletter Subscription Endpoint
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
