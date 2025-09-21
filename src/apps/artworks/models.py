from django.db import models


class Source(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    homepage_url = models.URLField(null=True, blank=True)
    
class Artist(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    death_year = models.PositiveIntegerField(null=True, blank=True) 
    nationality = models.CharField(max_length=50, null=True, blank=True)

class Artwork(models.Model):
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, related_name='artworks')
    source_id = models.CharField(max_length=100, db_index=True)
    uid = models.CharField(max_length=150, unique=True)
    
    title = models.CharField(max_length=500, db_index=True)
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, related_name='artworks')
    date = models.CharField(max_length=100, blank=True, null=True)
    year_start = models.PositiveIntegerField(null=True, blank=True)
    year_end = models.PositiveIntegerField(null=True, blank=True)
    medium = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=200, blank=True, null=True)
    
    collection = models.CharField(max_length=255, blank=True)
    credit_line = models.CharField(max_length=500, blank=True)
    license = models.CharField(max_length=100, blank=True)
    is_open_access = models.BooleanField(default=False)
    external_url = models.URLField(blank=True, null=True)
    
    image_url = models.URLField(blank=True, null=True)
    thumb_url = models.URLField(blank=True, null=True)
    image_attr = models.CharField(max_length=500, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Explanation(models.Model):
    artwork = models.OneToOneField(Artwork, on_delete=models.CASCADE, related_name='explanation')
    summary = models.TextField(blank=True)
    deep_explanation = models.TextField(blank=True)
    sources = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)