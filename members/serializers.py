from rest_framework import serializers

from core.serializers import SemesterSerializer
from core.serializers import UserSimpleSerializer
from members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer(read_only=True, required=False)
    seller = UserSimpleSerializer(read_only=True)
    last_edited_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Member
        fields = (
            "id",
            "name",
            "email",
            "date_joined",
            "semester",
            "lifetime",
            "honorary",
            "date_lifetime",
            "uio_username",
            "seller",
            "comments",
            "last_edited_by",
        )


class AddMemberSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=50, help_text="name of user, max 50 letters"
    )
    email = serializers.EmailField(allow_blank=True)
    lifetime = serializers.BooleanField(help_text="Is the member a lifetime member?")
    uio_username = serializers.CharField(
        max_length=15,
        allow_blank=True,
        required=False,
        help_text="Your Uio username. Is optional.",
    )


class MemberSimpleSerializer(serializers.Serializer):
    class Meta:
        model = Member
        fields = (
            "id",
            "name",
            "email",
            "date_joined",
            "semester",
            "lifetime",
            "honorary",
            "date_lifetime",
            "uio_username",
            "seller",
            "comments",
            "last_edited_by",
        )


class MemberSemesterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    semester = serializers.CharField()
    lifetime = serializers.IntegerField(
        help_text="Number of lifetimemembers sold that semester"
    )
    normal = serializers.IntegerField(
        help_text="Number of normal semester members that semester"
    )
    honorary = serializers.IntegerField(
        help_text="Number of honnorary memberships givenout that semester"
    )
