import csv
from decimal import Decimal

from django.db.models import Avg, Sum
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sales.models import Sale
from sales.serializers import SaleSerializer


class SaleList(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        if "file" not in request.FILES:
            return Response(
                {"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        csv_file = request.FILES["file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            row["user_id"] = request.user.id
            if isinstance(row["sales_number"], str):
                row["sales_number"] = int(Decimal(row["sales_number"]))
            serializer = self.get_serializer(data=row)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)


class SaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)


class SaleStatistics(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        current_user_sales = Sale.objects.filter(user_id=request.user.pk)
        average_sales_for_current_user = (
            current_user_sales
            .aggregate(Avg("sales_number"))
            .get("sales_number__avg", 0)
        )
        average_sale_all_user = (
            Sale
            .objects
            .all()
            .aggregate(Avg("sales_number"))
            .get("sales_number__avg", 0)
        )
        highest_revenue_sale_for_current_user = (
            current_user_sales
            .values("id", "revenue")
            .order_by("-revenue")
            .first()
        )
        product_highest_revenue_for_current_user = (
            current_user_sales
            .values("product")
            .annotate(total_revenue=Sum("revenue"))
            .order_by("-total_revenue")
            .first()
        )
        product_highest_sales_number_for_current_user = (
            current_user_sales
            .values("product")
            .annotate(total_sales=Sum("sales_number"))
            .order_by("-total_sales")
            .first()
        )

        response_data = {
            "average_sales_for_current_user": average_sales_for_current_user,
            "average_sale_all_user": average_sale_all_user,
            "highest_revenue_sale_for_current_user": {
                "sale_id": highest_revenue_sale_for_current_user["id"],
                "revenue": highest_revenue_sale_for_current_user["revenue"],
            },
            "product_highest_revenue_for_current_user": {
                "product_name": product_highest_revenue_for_current_user["product"],
                "revenue": product_highest_revenue_for_current_user["total_revenue"],
            },
            "product_highest_sales_number_for_current_user": {
                "product_name": product_highest_sales_number_for_current_user[
                    "product"
                ],
                "sales_number": product_highest_sales_number_for_current_user[
                    "total_sales"
                ],
            },
        }

        return Response(response_data)
