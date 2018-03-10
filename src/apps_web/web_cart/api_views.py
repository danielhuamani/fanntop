from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from apps_base.cart.cart import CartObject
from apps_base.cart.models import Cart
from django.utils.translation import ugettext_lazy as _
from .serializers import CartSerializer


class CartAPI(APIView):
    # queryset = Cart.objects.none()

    def get(self, request, format=None):
        code = request.COOKIES.get('cart', None)
        cart_object = CartObject(code)
        if cart_object.validate_code():
            cart = cart_object.get_cart()
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=200)
        else:
            data = {}
            return Response(data, status=403)

    def post(self, request, format=None):
        code = request.COOKIES.get('cart', None)
        cart_object = CartObject(code)
        sku = request.data.get('sku', '')
        quantity = request.data.get('quantity', 0)
        error = ''
        if cart_object.validate_code():
            if cart_object.validate_product(sku, quantity):
                if cart_object.validate_sku_quantity_product(sku, quantity):
                    cart_object.add_cart_item(sku, quantity)
                    cart = cart_object.get_cart()
                    serializer = CartSerializer(cart)
                    response = Response(serializer.data, status=200)
                    response.set_cookie('cart', cart.code, max_age=60*60*24*2)
                    return response
                else:
                    error = _('No stock available')
            else:
                error = _('There was an error in the shopping cart')
        else:
            if cart_object.validate_product(sku, quantity):
                if cart_object.validate_sku_quantity_product(sku, quantity):
                    cart_object.create_cart()
                    cart_object.add_cart_item(sku, quantity)
                    cart = cart_object.get_cart()
                    serializer = CartSerializer(cart)
                    response = Response(serializer.data, status=200)
                    response.set_cookie('cart', cart.code)
                    return response
                else:
                    error = _('No stock available')
            else:
                error = _('There was an error in the shopping cart')

        data = {
            'error': error
        }
        return Response(data, status=403)

    def delete(self, request, format=None):
        code = request.COOKIES.get('cart', None)
        cart_object = CartObject(code)
        sku = request.data.get('sku', '')
        error = ''
        if cart_object.validate_code():
            if cart_object.validate_exist_product(sku):
                cart_object.delete_cart_item(sku)
                cart = cart_object.get_cart()
                serializer = CartSerializer(cart)
                response = Response(serializer.data, status=200)
                return response
            else:
                error = _('There was an error in the shopping cart')
        else:
            error = _('There was an error in the shopping cart')
        data = {
            'error': error
        }
        return Response(data, status=403)