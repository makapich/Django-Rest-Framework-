from blog_api.views import CommentDetailUpdateAPIView, PublicationViewSet

from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework.authtoken import views


router = routers.DefaultRouter()
router.register(r'publications', PublicationViewSet, basename='publication')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.ObtainAuthToken.as_view()),
    path('', include(router.urls)),
    path('comments/<int:pk>/', CommentDetailUpdateAPIView.as_view(), name='comment-detail'),

]