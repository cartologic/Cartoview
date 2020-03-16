from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import (FieldPanel, ObjectList,
                                         StreamFieldPanel, TabbedInterface)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from .blocks.Blocks import HeroAreaBlock, MapCatalogBlock
from .blocks.ImageTextOverlayBlock import ImageTextOverlayBlock
from .blocks.ThumbnailGalleryBlock import ThumbnailGalleryBlock
from .grid.GridBlock import GridBlock
from .blocks.ImageLinkGalleryBlock import ImageLinkGalleryBlock


class HomePage(Page):
    parent_page_types = ['LanguageRedirectionPage']
    hero = StreamField([
        ('hero_area', HeroAreaBlock()),
    ], blank=True, null=True, help_text=mark_safe("You should add only <b>1 Hero</b>"))
    body = StreamField([
        ('map_catalog', MapCatalogBlock()),
        ('image_link_gallery', ImageLinkGalleryBlock()),
        ('grid', GridBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image_text_overlay', ImageTextOverlayBlock()),
        ('thumbnail_gallery', ThumbnailGalleryBlock()),
    ], blank=True, null=True)
    selected_template = models.CharField(max_length=255, choices=(
        ('cms/home_page_default.html', 'Default Template'),
    ), default='cms/home_page_default.html')

    @property
    def template(self):
        return self.selected_template

    content_panels = [
        FieldPanel('title', classname="full title"),
        StreamFieldPanel("hero", classname="Full"),
        StreamFieldPanel("body", classname="Full"),
    ]
    theme_panels = [
        FieldPanel('selected_template', widget=forms.Select),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    class Meta:
        verbose_name = "Site Homepage"