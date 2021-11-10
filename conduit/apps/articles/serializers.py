from rest_framework import serializers

from conduit.apps.profiles.serializers import ProfileSerilizer

from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerilizer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)

    createdAt = serializers.SerializerMethodField(method_name='get_create_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')


    class Meta:
        model = Article
        fields = (
            'author',
            'body',
            'createdAt',
            'description',
            'slug',
            'title',
            'updatedAt',
        )

    def create(self, validated_data):
        author = self.context.get('author', None)

        return Article.objects.create(author=author, **validated_data)

    def get_create_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerilizer(required=False)

    createdAt = serializers.SerializerMethodField(method_name='get_create_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'body',
            'createdAt',
            'updatedAt'
        )

        def create(self, validated_data):
            article = self.context['article']
            author = self.context['author']

            return Comment.objects.create(
                author=author, article=article, **validated_data
            )

        def get_create_at(self, instance):
            return instance.created_at.isoformat()

        def get_updated_at(self, instace):
            return instace.updated_at.isoformat()
