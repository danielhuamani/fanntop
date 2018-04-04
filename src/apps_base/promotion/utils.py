from .models import CouponGenerate
import uuid

def generate_code_coupon(coupon, quantity_generate):
    prefix = coupon.prefix.strip()
    prefix = prefix + '-'
    list_coupon_generate = []
    for generate in range(quantity_generate):
        code = prefix + uuid.uuid4().hex[:9].lower()
        list_coupon_generate.append(CouponGenerate(code=code, coupon=coupon))
    CouponGenerate.objects.bulk_create(list_coupon_generate)