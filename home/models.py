from django.db import models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class HomePage(Page):
    """
    The home page model - the root page of the website
    """
    
    # Define the fields that appear in the admin
    body = RichTextField(
        blank=True,
        help_text="The main content for the home page"
    )
    
    # Tell Wagtail which fields to show in the editor
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    # This makes the HomePage template use a specific template
    template = 'home/home_page.html'
    
    class Meta:
        verbose_name = "Home Page"
