from django.contrib.auth import get_user_model
from rest_framework import serializers

from sales.models import Sale


class SaleSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), source='user')

    class Meta:
        model = Sale
        fields = ("id", "date", "product", "sales_number", "revenue", "user_id")
