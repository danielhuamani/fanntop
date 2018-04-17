from rest_framework.views import APIView
from rest_framework.response import Response
from apps_base.shipping.models import ShippingCost
from apps_base.customers.models import CustomerShippingAddress
from .serializers import CustomerShippingAddressSerializer


class CustomerShippingAddressAPI(APIView):
    # queryset = Cart.objects.none()

    def get(self, request, format=None):
        address = request.query_params.get('address', None)
        if address:
            try:
                customer_shipping_addres = CustomerShippingAddress.objects.get(
                    id=int(address))
                serializer = CustomerShippingAddressSerializer(customer_shipping_addres)
                return Response(serializer.data, status=200)
            except Exception as e:
                return Response({}, status=403)
        return Response({}, status=403)