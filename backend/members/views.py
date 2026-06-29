from rest_framework import viewsets, filters
from .models import Membership, Member, Staff
from .serializers import MembershipSerializer, MemberSerializer, StaffSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related("membership").all()
    serializer_class = MemberSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "email"]


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
