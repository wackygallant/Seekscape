from django.db import models
from tinymce.models import HTMLField

from utils.models import BaseModel
from django.utils.text import slugify

class Trek(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    duration = models.PositiveIntegerField(help_text='In days')
    distance = models.PositiveIntegerField(help_text='In kms')
    description = models.TextField()
    
    DIFFICULTY = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY)
    
    image = models.ImageField(upload_to='trek_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    itinerary = HTMLField()
    
    map_embed_url = models.TextField(
        null=True, 
        blank=True, 
        help_text="Google My Maps 'Embed on my site' URL (only the src link inside the iframe)"
    )
    
    def save(self, *args, **kwargs):
        # 1. Corrected: Use self.title
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        
        # 2. Add the Map URL auto-fix logic we discussed earlier!
        if self.map_embed_url and "/viewer?" in self.map_embed_url:
            self.map_embed_url = self.map_embed_url.replace("/viewer?", "/embed?")
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Trek'
        verbose_name_plural = 'Treks'
        db_table = 'trek'