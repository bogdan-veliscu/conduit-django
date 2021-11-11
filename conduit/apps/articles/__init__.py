from django.apps import AppConfig


class ArticlesAppConfig(AppConfig):
    name = 'conduit.apps.articles'
    default_auto_field = 'django.db.models.AutoField'
    label = 'articles'
    verbose_name = 'Articles'


    def ready(self):
        import conduit.apps.articles.signals


default_app_config = 'conduit.apps.articles.ArticlesAppConfig'
