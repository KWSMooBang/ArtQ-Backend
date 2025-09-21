from rest_framework import serializers
from .models import Source, Artist, Artwork, Explanation


class ShowArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'birth_year', 'death_year', 'nationality', 'image_url', 'thumb_url', 'image_attr']

class ShowArtworkSerializer(serializers.ModelSerializer):
    artist = ShowArtistSerializer()
    class Meta:
        model = Artwork
        fields = ['title', 'artist', 'date', 'medium', 'size', 'collection', 'credit_line', 'license', 'is_open_access', 'external_url', 'image_url', 'thumb_url', 'image_attr']
        
class ShowExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Explanation
        fields = ['summary', 'deep_explanation', 'sources', 'updated_at']