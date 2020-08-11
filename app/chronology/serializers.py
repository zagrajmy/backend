from rest_framework import serializers

from .models import Proposal, WaitList


class WaitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitList
        fields = "__all__"


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        exclude = ["created_at"]

    speaker_name = serializers.CharField(max_length=255, required=False)

    def validate(self, attrs: dict) -> dict:
        data: dict = super().validate(attrs)
        if not data.get("speaker_name"):
            user = data.get("speaker_user")
            if not user:
                raise serializers.ValidationError("No speaker name nor speaker user")
            data["speaker_name"] = str(user)

        return data
