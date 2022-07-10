from rest_framework import serializers

from chat.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
	user = serializers.CharField(source='user.email')

	class Meta:
		model = ChatMessage
		fields = "__all__"