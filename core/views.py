from django.shortcuts import render, redirect, get_object_or_404
from core.models import GeneralSetting, ImageSetting, Skill, Experience, Education, SocialMedia, Document
from contact.forms import ContactForm
# Create your views here.
def layout(request):
    site_title = GeneralSetting.objects.get(name='site_title').parameter
    site_keywords = GeneralSetting.objects.get(name='site_keywords').parameter
    site_description = GeneralSetting.objects.get(name='site_description').parameter
    home_banner_name = GeneralSetting.objects.get(name='home_banner_name').parameter
    home_banner_title = GeneralSetting.objects.get(name='home_banner_title').parameter
    home_banner_description = GeneralSetting.objects.get(name='home_banner_description').parameter

    # Images
    header_logo = ImageSetting.objects.get(name='header_logo').file
    home_banner_image = ImageSetting.objects.get(name='home_banner_image').file
    site_favicon = ImageSetting.objects.get(name='site_favicon').file

    #Documents
    documents = Document.objects.all()

    # Social Media
    social_medias = SocialMedia.objects.all()

    context = {
        'site_title': site_title,
        'site_keywords': site_keywords,
        'site_description': site_description,
        'home_banner_name': home_banner_name,
        'home_banner_title': home_banner_title,
        'home_banner_description': home_banner_description,
        'home_banner_image': home_banner_image,
        'header_logo': header_logo,
        'site_favicon': site_favicon,
        'documents': documents,
        'social_medias': social_medias,
    }
    return context

def index(request):

    #Skills
    skills = Skill.objects.all().order_by('order')

    #Experiences
    experiences = Experience.objects.all()

    #Educations
    educations = Education.objects.all()

    contact_form = ContactForm()

    context = {
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'contact_form': contact_form,
    }
    return render(request, 'index.html',context=context)

def redirect_urls(request, slug):
    doc = get_object_or_404(Document, slug=slug)
    return redirect(doc.file.url)


