from rest_framework import serializers
from .models import Membership, Member, Staff


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ["id", "type_name", "loan_limit", "loan_duration_days", "can_reserve"]


class MemberSerializer(serializers.ModelSerializer):
    membership_name = serializers.CharField(source="membership.type_name", read_only=True)
    active_loan_count = serializers.IntegerField(read_only=True)
    can_borrow = serializers.BooleanField(read_only=True)

    class Meta:
        model = Member
        fields = [
            "id", "name", "email", "phone", "address",
            "membership", "membership_name", "membership_date",
            "status", "active_loan_count", "can_borrow",
        ]


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "name", "email", "role"]
