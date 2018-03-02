<template>
  <section class="main car">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <div class="title-page">
            <h2><i class="fa fa-shopping-bag"> </i>MI COMPRA</h2>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="boxw box-car">
            <div class="inner">
              <table border="1" cellpadding="0" cellspacing="0" style="width: 100%;" class="tbl-car">
                <thead>
                  <tr>
                    <th valign="top" class="product-item">Producto</th>
                    <th valign="top" class="price">Precio</th>
                    <th valign="top" class="quantity">Cantidad</th>
                    <th valign="top" width="15%" class="subtotal">Subtotal</th>
                    <th valign="top"  class="delete"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="item-car" v-for='item in getCart.cart_items'>
                    <td valign="center">
                      <div class="detail-car">
                        <div class="image"><a href="#"><img :src="item.image" /></a></div>
                        <div class="detail">
                          <h3>{{item.product_name}}</h3>
                          <div class="sku">SKU: 13006893</div>
                        </div>
                      </div>
                    </td>
                    <td valign="center">
                      <div class="w-price">
                        <div class="price-promo">

                          Precio: <span class="price">S/ {{item.product_price}}</span>
                        </div>
                        <!-- <div class="price-normal">Precio regular: <span class="trought">S/ 399.00</span><span class="precio-percentage">-12%</span></div> -->
                      </div>
                    </td>
                    <td valign="center">
                      <div class="w-quantity">
                        <div class="quantity-control min">
                          <a class="menos" @click='quantityMenos(item.quantity, item.product_sku)'><i class="fa fa-minus"></i></a>
                          <input class="select-number" :value='item.quantity' readonly/>
                          <a @click.prevent='quantityMas(item.quantity, item.product_sku)' class="menos"><i class="fa fa-plus"></i></a>
                        </div>
                      </div>
                    </td>
                    <td valign="center">
                      <div class="w-subtotal"><span class="st">S/. {{item.cart_item_total}}</span></div>
                    </td>
                    <td valign="center">
                      <div class="w-delete"><a href="#" @click.prevent='deleteCartItem(item.product_sku)'><i class="fa fa-times"></i></a></div>
                    </td>
                  </tr>

                  <tr>
                    <td valign="center"><a href="/">Continue Comprando</a></td>
                    <td valign="center" colspan="2"></td>
                    <td valign="center" colspan="2">
                      <div class="w-total"><span class="to">Total:   <strong>S/. {{getCart.total}}</strong></span></div>
                    </td>
                  </tr>

                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="w-btn w-btn-car"><a class="btn btn-primary">Ir a Comprar</a></div>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
  export default {
    name: 'cart',
    created () {
      this.$store.dispatch('getCartView')
    },
    methods: {
      quantityMenos (quantity, sku) {
        if (quantity - 1 > 0) {
          this.$store.dispatch('purchase', {
            sku: sku,
            quantity: quantity - 1,
            notMenu: true
          })
        }
      },
      quantityMas (quantity, sku) {
        this.$store.dispatch('purchase', {
          sku: sku,
          quantity: quantity + 1,
          notMenu: true
        })
      },
      deleteCartItem (sku) {
        this.$store.dispatch('deleteCartItem', {
          sku: sku,
          notMenu: true
        })
      }
    },
    computed: {
      getCart () {
        return this.$store.getters.getCart
      }
    }
  }
</script>
<style lang='scss'>
  .item-car .detail{
    padding: 0;
  }
</style>