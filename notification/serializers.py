from rest_framework import serializers

from user.serializers import UserSerializer
from badge.serializers import BadgeSerializer
from feed.serializers import PostSerializer, CommentSerializer
from notification.models import *


class NotificationSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    user = UserSerializer(source="arg_user")
    feed = PostSerializer(source="arg_feed")
    comment = CommentSerializer(source="arg_comment")
    badge = BadgeSerializer(source="arg_badge")

    class Meta:
        model = Notification
        fields = ['type', 'user', 'feed', 'comment', 'badge']
