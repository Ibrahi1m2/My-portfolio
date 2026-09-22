import re
import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.core.validators import validate_email, ValidationError
from .models import ContactMessage, NewsletterSubscriber

logger = logging.getLogger(__name__)

# -----------------------------------------------
# Home Page
# -----------------------------------------------
def index(request):
    """Portfolio home page view"""
    context = {
        'page_title': 'Home | My Portfolio',
    }
    return render(request, 'index.html', context)


# -----------------------------------------------
# Blog List Page
# -----------------------------------------------
def blog(request):
    """Blog listing page view"""
    context = {
        'page_title': 'Blog | My Portfolio',
    }
    return render(request, 'blog.html', context)


# -----------------------------------------------
# Blog Detail Page
# -----------------------------------------------
def blog_details(request):
    """Blog detail page view"""
    context = {
        'page_title': 'Blog Details | My Portfolio',
    }
    return render(request, 'blog-details.html', context)


# -----------------------------------------------
# Contact Page
# -----------------------------------------------
def contact(request):
    """Contact page view"""
    context = {
        'page_title': 'Contact | My Portfolio',
    }
    return render(request, 'contact.html', context)


# -----------------------------------------------
# Service Details Page
# -----------------------------------------------
def service_details(request):
    """Service details page view"""
    context = {
        'page_title': 'Service Details | My Portfolio',
    }
    return render(request, 'service-details.html', context)
def index_02(request):
    """Portfolio home page view"""
    context = {
        'page_title': 'Home | My Portfolio',
    }
    return render(request, 'index-02.html', context)
def index_03(request):
    """Portfolio home page view"""
    context = {
        'page_title': 'Home | My Portfolio',
    }
    return render(request, 'index-03.html', context)
def index_04(request):
    """Portfolio home page view"""
    context = {
        'page_title': 'Home | My Portfolio',
    }
    return render(request, 'index-04.html', context)
def index_05(request):
    """Portfolio home page view"""
    context = {
        'page_title': 'Home | My Portfolio',
    }
    return render(request, 'index-05.html', context)
def index_06(request):  
    """Portfolio home page view"""
    context = {
        'page_title': 'Home | My Portfolio',
    }
    return render(request, 'index-06.html', context)
def index_07(request):
    """Portfolio home page view"""
    context = {
        'page_title': 'Home | My Portfolio',
    }
    return render(request, 'index-07.html', context)
def index_08(request):
    """Portfolio home page view"""
    context = {
        'page_title': 'Home | My Portfolio',
    }
    return render(request, 'index-08.html', context)
def index_09(request):
    """Portfolio home page view"""
    context = {
        'page_title': 'Home | My Portfolio',
    }
    return render(request, 'index-09.html', context)


# -----------------------------------------------
# Contact Form Submission Handler
# -----------------------------------------------
def contact_submit(request):
    """Handle portfolio contact form submission via AJAX or regular POST."""
    if request.method != 'POST':
        return HttpResponse('Invalid request method. Only POST is allowed.', status=405)

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()

    # --- Strict Server-side Validation ---
    # 1. Name validation
    if len(name) < 2:
        return HttpResponse('Please enter your full name (at least 2 characters).', status=400)

    # 2. Email validation (must have @ and valid domain extension like .com)
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return HttpResponse('Please enter a valid and complete email address (e.g., name@gmail.com).', status=400)
    try:
        validate_email(email)
    except ValidationError:
        return HttpResponse('Please enter a valid email address.', status=400)

    # 3. Phone number validation (strictly 10 digits)
    cleaned_phone = re.sub(r'\D', '', phone)
    if len(cleaned_phone) != 10:
        return HttpResponse('Please enter a valid 10-digit phone number (exactly 10 digits).', status=400)

    # 4. Message validation (between 10 and 500 characters)
    if len(message) < 10:
        return HttpResponse('Please enter a meaningful message of at least 10 characters.', status=400)
    if len(message) > 500:
        return HttpResponse('Message cannot exceed 500 characters.', status=400)

    # 1. Save to Database so no message is ever lost
    try:
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
    except Exception as e:
        logger.error(f"Error saving contact message to DB: {e}")

    # 2. Render and Dispatch Email Notification to iburahim004@gmail.com
    now = timezone.localtime(timezone.now()) if timezone.is_aware(timezone.now()) else timezone.now()
    formatted_time = now.strftime("%B %d, %Y at %I:%M %p")

    try:
        host = request.get_host()
    except Exception:
        host = 'localhost'

    context = {
        'name': name,
        'email': email,
        'phone': phone,
        'subject': subject,
        'message': message,
        'timestamp': formatted_time,
        'host': host,
    }

    recipient_email = getattr(settings, 'PORTFOLIO_OWNER_EMAIL', 'iburahim004@gmail.com')
    sender_account = getattr(settings, 'EMAIL_HOST_USER', recipient_email)
    from_email = f'"{name} (via Portfolio)" <{sender_account}>'

    try:
        email_subject = f"📩 New Inquiry from {name}"
        if subject:
            email_subject += f" - {subject}"


        html_content = render_to_string('emails/contact_notification.html', context)
        text_content = render_to_string('emails/contact_notification.txt', context)

        mail = EmailMultiAlternatives(
            subject=email_subject,
            body=text_content,
            from_email=from_email,
            to=[recipient_email],
            reply_to=[email],
        )
        mail.attach_alternative(html_content, "text/html")
        mail.send(fail_silently=False)
    except Exception as e:
        logger.warning(f"Note: Email dispatch attempted to {recipient_email}. Reason: {e}")

    success_msg = "Thank you! Your message has been sent successfully. I will get back to you shortly."

    # Return text or JSON based on request
    if 'application/json' in request.headers.get('Accept', ''):
        return JsonResponse({'status': 'success', 'message': success_msg})

    return HttpResponse(success_msg, status=200)


# -----------------------------------------------
# Newsletter Subscription Handler
# -----------------------------------------------
def newsletter_subscribe(request):
    """Handle footer newsletter subscription via AJAX."""
    if request.method != 'POST':
        return HttpResponse('Invalid request method. Only POST is allowed.', status=405)

    email = request.POST.get('email', '').strip()

    # Strict Email Validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not re.match(email_regex, email):
        return HttpResponse('Please enter a valid email address (e.g. name@gmail.com).', status=400)
    try:
        validate_email(email)
    except ValidationError:
        return HttpResponse('Please enter a valid email address.', status=400)

    # Check if already subscribed
    existing = NewsletterSubscriber.objects.filter(email__iexact=email).first()
    if existing:
        return HttpResponse("You are already subscribed to the newsletter! Thank you for your support.", status=200)

    # Save to Database
    try:
        NewsletterSubscriber.objects.create(email=email)
    except Exception as e:
        logger.error(f"Error saving newsletter subscriber: {e}")

    # Dispatch Notification Email to iburahim004@gmail.com
    now = timezone.localtime(timezone.now()) if timezone.is_aware(timezone.now()) else timezone.now()
    formatted_time = now.strftime("%B %d, %Y at %I:%M %p")

    recipient_email = getattr(settings, 'PORTFOLIO_OWNER_EMAIL', 'iburahim004@gmail.com')
    sender_account = getattr(settings, 'EMAIL_HOST_USER', recipient_email)
    from_email = f'"Portfolio Newsletter" <{sender_account}>'

    try:
        email_subject = f"⚡ New Newsletter Subscriber: {email}"
        email_body = f"""Hello Ibrahim,\n\nGreat news! A new subscriber has joined your portfolio newsletter from your website footer.\n\nSubscriber Email: {email}\nSubscribed At: {formatted_time}\n\nYou can manage all subscribers in your Django Admin dashboard.\n\nBest regards,\nYour Portfolio Website\n"""
        mail = EmailMultiAlternatives(
            subject=email_subject,
            body=email_body,
            from_email=from_email,
            to=[recipient_email],
            reply_to=[email],
        )
        mail.send(fail_silently=False)
    except Exception as e:
        logger.warning(f"Note: Email dispatch attempted to {recipient_email}. Reason: {e}")

    success_msg = "Thank you! You have successfully subscribed to my newsletter."
    if 'application/json' in request.headers.get('Accept', ''):
        return JsonResponse({'status': 'success', 'message': success_msg})

    return HttpResponse(success_msg, status=200)