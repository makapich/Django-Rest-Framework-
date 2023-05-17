from blog_api.models import Comment, Publication
from blog_api.permissions import IsOwnerOrReadOnly
from blog_api.serializers import CommentSerializer, PublicationSerializer

from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response


User = get_user_model()


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all().order_by('-created_at')
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, methods=['GET', 'POST', 'DELETE'], serializer_class=CommentSerializer)
    def comment(self, request, pk=None):
        if self.request.method == 'GET':
            publication = self.get_object()
            comments = Comment.objects.filter(publication=publication).order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        if self.request.method == 'POST':
            publication = self.get_object()
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(publication=publication, author=request.user)
                return redirect('publication-detail', pk=publication.pk)
            return Response(serializer.errors, status=400)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return redirect('publication-list')


class CommentDetailUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]