from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, CommentListCreateAPIView

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)

app_name = 'articles'
urlpatterns = [
    path('', include(router.urls)),
    path(
        'articles/<slug:article_slug>/comments',
        CommentListCreateAPIView.as_view()
    )
]
