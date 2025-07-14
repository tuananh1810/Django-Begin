from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ProductView(APIView):
    permission_classes = [IsAuthenticated]  # Hoặc dùng custom permission

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # ✅ Trường hợp gửi 1 sản phẩm
        if isinstance(data, dict):
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Trường hợp gửi nhiều sản phẩm (bulk)
        elif isinstance(data, list):
            for item in data:
                item['created_by'] = request.user.id  # gán người tạo
            serializer = ProductSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Dữ liệu không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)