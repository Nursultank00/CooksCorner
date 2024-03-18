from rest_framework.views import Response, status, APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import Receipt, Category
from .serializers import (
                        ReceiptSerializer, 
                        AddReceiptSerializer, 
                        IngredientSerializer, 
                        ReceiptCreateSerializer,
                        CategorySerializer
)
# Create your views here.
class GetReceiptAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Receipts'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "подробную информацию "
                              "о рецепте.",                    
        responses = {
            200: ReceiptSerializer,
            404: "Receipt is not found.",
        },
    )
    def get(self, request, slug, *args, **kwargs):
        try:
            receipt = Receipt.objects.get(slug = slug)
        except Exception:
            return Response({"Error": "Receipt is not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReceiptSerializer(receipt, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddReceiptAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Receipts'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность создать "
                              "новый рецепт.",
        request_body = AddReceiptSerializer,                   
        responses = {
            201: "Receipt is created.",
            400: "Invalid data.",
        },
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.profile.id
        ingredients = data.pop('ingredients')
        ingred_serializer = IngredientSerializer(data = ingredients, many = True)
        ingred_serializer.is_valid(raise_exception = True)
        serializer = ReceiptCreateSerializer(data = data)
        serializer.is_valid(raise_exception = True)
        receipt = serializer.save()
        for item in ingred_serializer.validated_data:
            item['receipt'] = receipt
        ingred_serializer.save()
        return Response({"Message": "Receipt is created."}, status=status.HTTP_201_CREATED)
        
class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Receipts'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "все категории рецептов. ",              
        responses = {
            200: CategorySerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
        