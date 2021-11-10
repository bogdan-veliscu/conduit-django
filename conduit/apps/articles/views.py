from rest_framework import mixins, generics, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Article, Comment
from .renderers import ArticleJSONRenderer, CommentJSONRenderer
from .serializers import ArticleSerializer, CommentSerializer


class ArticleViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    lookup_field = 'slug'
    queryset = Article.objects.select_related('author', 'author__user')
    permissions_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer


    def create(self, request):
        serializer_context = {'author': request.user.profile}
        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            serializer_instance, data=serializer_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = 'article__slug'
    lookup_url_kwargs = 'article_slug'
    permissions_classes = (IsAuthenticatedOrReadOnly,)
    queryset= Comment.objects.select_related(
        'article', 'article__author', 'article__author__user',
        'author', 'author__user'
    )
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer


    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwargs]}

        return queryset.filter(**filters)

    def create(self, request, article_slug=None):
        data = request.data.get('comment',{})
        context = {'author': request.user.profile}

        try:
            context['article'] = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

