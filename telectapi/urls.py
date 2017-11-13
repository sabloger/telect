from django.conf.urls import include, url
from rest_framework import routers

from telectapi.api.v1.channel import TgChannel
from telectapi.api.v1.collection import Collection
from telectapi.api.v1.collection_source import CollectionSource
from telectapi.api.v1.user import User

router = routers.DefaultRouter()
router.register(r'user', User, "user")
router.register(r'collection', Collection, "collection")
router.register(r'channel', TgChannel, "channel")
router.register(r'source', CollectionSource, "source")

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^col$', views.col, name='col'),
    # url(r'^send$', views.send, name='send'),
    # url(r'^chan$', views.chan, name='chan'),
    # url(r'^bot$', views.bot, name='bot'),
    #
    # url(r'^api/v1/user/auth$', user.auth, name='user.auth'),

    url(r'^api/v1/', include(router.urls, namespace='api.v1')),
]

# urlpatterns += router.urls

# ^ ^api/v1/ ^user/$ [name='user-list']
# ^ ^api/v1/ ^user\.(?P<format>[a-z0-9]+)/?$ [name='user-list']
# ^ ^api/v1/ ^user/auth/$ [name='user-auth']
# ^ ^api/v1/ ^user/auth\.(?P<format>[a-z0-9]+)/?$ [name='user-auth']
# ^ ^api/v1/ ^$ [name='api-root']
# ^ ^api/v1/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']
# ^admin/
