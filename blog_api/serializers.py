from blog_api.models import Comment, Publication

from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class PublicationSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    link = serializers.HyperlinkedIdentityField(view_name='publication-detail')

    class Meta:
        model = Publication
        fields = ['title', 'description', 'author', 'created_at', 'link', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    publication = serializers.ReadOnlyField(source='publication.id')
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Comment
        fields = ['publication', 'author', 'text', 'created_at']