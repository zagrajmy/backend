from typing import Optional, TypedDict

from rest_framework import serializers

from crowd.models import User

from .models import Proposal, WaitList


class WaitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitList
        fields = "__all__"


class ProposalTypedDict(TypedDict):
    speaker_name: Optional[str]
    speaker_user: Optional[User]


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        exclude = ["created_at"]

    speaker_name = serializers.CharField(max_length=255, required=False)

    def validate(self, attrs: ProposalTypedDict) -> ProposalTypedDict:
        data: ProposalTypedDict = super().validate(  # type: ignore[no-untyped-call]
            attrs,
        )
        if not data.get("speaker_name"):
            user = data.get("speaker_user")
            if not user:
                raise serializers.ValidationError("No speaker name nor speaker user")
            data["speaker_name"] = str(user)

        return data
