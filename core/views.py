from django.shortcuts import render, redirect, get_object_or_404
from core.models import GeneralSetting, ImageSetting, Skill, Experience, Education, SocialMedia, Document
from contact.forms import ContactForm
from core import models as core_models
from django.http import Http404
from core import models
# Create your views here.

def get_general_setting(parameter):
    try:
        obj = GeneralSetting.objects.get(name=parameter).parameter
    except:
        obj = ''
    return obj


def get_image_setting(parameter):
    try:
        obj = ImageSetting.objects.get(name=parameter).file
    except:
        obj = ''
    return obj


def layout(request):
    site_title = get_general_setting('site_title')
    site_keywords = get_general_setting('site_keywords')
    site_description = get_general_setting('site_description')
    home_banner_name = get_general_setting('home_banner_name')
    home_banner_title = get_general_setting('home_banner_title')
    home_banner_description = get_general_setting('home_banner_description')

    # Images
    header_logo = get_image_setting('header_logo')
    home_banner_image = get_image_setting('home_banner_image')
    site_favicon = get_image_setting('site_favicon')

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

def create_statistic(request, statistic_type, action, source):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')

        core_models.Statistics.objects.create(
            statistic_type=statistic_type,
            action=action,
            source=source,
            ip_address=ipaddress,
            user_agent=request.META.get('HTTP_USER_AGENT'),
        )
    except:
        pass


def special_links(request, slug):
    """
    Checks first if slug is in Document objects. If not then checks in images.
    Returns the file of object from slug field.
    """

    obj = None
    obj_type = None
    try:
        redirect_source = 'popup' if '_popup' in slug else 'direct_link'
        slug = slug.replace('_popup', '')
        obj = models.RedirectSlug.objects.get(slug=slug)
        create_statistic(request, 'RedirectSlug', f'Click slug: {slug}', redirect_source)
        return redirect(obj.new_url)
    except models.RedirectSlug.DoesNotExist:
        pass

    try:
        obj = core_models.Document.objects.get(name=slug)
        obj_type = 'doc'
    except core_models.Document.DoesNotExist:
        pass

    if not obj:
        try:
            obj = core_models.ImageSetting.objects.get(name=slug)
            obj_type = 'image'
        except core_models.ImageSetting.DoesNotExist:
            pass

    if obj:
        if obj_type == 'doc':
            if obj.file:
                create_statistic(request, 'Document', f'Click slug: {slug}', 'direct_link')
                return redirect(obj.file.url)
        elif obj_type == 'image':
            if obj.file:
                context = {
                    'object': obj,
                }
                create_statistic(request, 'ImageSetting', f'Click slug: {slug}', 'direct_link')
                return render(request, 'image.html', context=context)
        return redirect('index')
    else:
        raise Http404
