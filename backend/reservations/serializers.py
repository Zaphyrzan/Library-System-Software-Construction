from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    member_name = serializers.CharField(source="member.name", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id", "book", "book_title", "member", "member_name",
            "reservation_date", "queue_position", "status",
        ]
        read_only_fields = ["reservation_date", "queue_position", "status"]
