from rest_framework import serializers
from .models import Fine, Notification


class FineSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source="loan.member.name", read_only=True)
    book_title = serializers.CharField(source="loan.copy.book.title", read_only=True)

    class Meta:
        model = Fine
        fields = [
            "id", "loan", "member_name", "book_title", "amount",
            "reason", "issued_date", "paid", "payment_date",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source="member.name", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "member", "member_name", "message", "sent_date", "read"]
