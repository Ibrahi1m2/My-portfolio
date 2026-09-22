from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Home Page → /
    path('', views.index, name='index'),
    path('index-02/', views.index_02, name='index-02'),
    path('index-03/', views.index_03, name='index-03'),
    path('index-04/', views.index_04, name='index-04'),
    path('index-05/', views.index_05, name='index-05'),
    path('index-06/', views.index_06, name='index-06'),
    path('index-07/', views.index_07, name='index-07'),
    path('index-08/', views.index_08, name='index-08'),
    path('index-09/', views.index_09, name='index-09'),
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
