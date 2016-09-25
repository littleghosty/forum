from django.conf.urls import url
from .views import article_list, create_article

urlpatterns = [
        url(r'^list/(?P<block_id>\d+)', article_list, name="article_list"),
        url(r'^list/create/(?P<block_id>\d+)', create_article, name="create_article"),
]
