<template>
  <div class="cart-view " :class="[getStatusCartView ? '' : 'cart-view--inactive']">


    <div class="cart-view__overlay" @click.prevent='changeStatusCartView'>

    </div>
    <div class="cart-view__error" v-if='getError'>
      <h4>{{getError}}dd</h4>
    </div>
    <div class="box-caritem  boxw">
      <div class="inner">
        <div class="title">
          <h3><i class="fa fa-shopping-bag"> </i>MI COMPRA  </h3>
        </div>
        <div class="itemcar-body" v-if='getCart.cart_items.length > 0'>
          <div class="item-car" v-for='item in getCart.cart_items'>
            <div class="item"><a href="">
                <div class="image"><img :src="item.image" width="60"/></div></a></div>
            <div class="detail">
              <h3>{{item.product_name}}</h3>
              <div class="price">Precio: <strong>S/. {{item.product_price}}</strong></div>
              <div class="w-quantity">
                <div class="quantity-control min">
                  <a class="menos" @click.prevent='quantityMenos(item.quantity, item.product_sku)'><i class="fa fa-minus"></i></a>
                  <input class="select-number" :value='item.quantity' /><a class="menos" @click.prevent='quantityMas(item.quantity, item.product_sku)'><i class="fa fa-plus"></i></a>
                </div>
              </div>
              <div class="w-remove"><a href="" @click.prevent='deleteCartItem(item.product_sku)'>eliminar</a></div>
            </div>
          </div>
        </div>
        <div class="totals" v-if='getCart.cart_items.length > 0'>
          <div class="subtotal">
            <div class="title-s">Subtotal: </div><strong>S/. {{getCart.total}}</strong>
          </div>
          <div class="w-btn"><a class="btn btn-primary">Ver Carrito</a></div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'cartView',
    data () {
      return {

      }
    },
    methods: {
      changeStatusCartView () {
        this.$store.dispatch('changeStatusCartView', false, false)
      },
      quantityMenos (quantity, sku) {
        if (quantity - 1 > 0) {
          this.$store.dispatch('purchase', {
            sku: sku,
            quantity: quantity - 1
          })
        }
      },
      quantityMas (quantity, sku) {
        this.$store.dispatch('purchase', {
          sku: sku,
          quantity: quantity + 1
        })
      },
      deleteCartItem (sku) {
        this.$store.dispatch('deleteCartItem', {
          sku: sku,
        })
      }
    },
    computed: {
      getStatusCartView () {
        return this.$store.getters.getStatusCartView
      },
      getCart () {
        return this.$store.getters.getCart
      },
      getError () {
        return this.$store.getters.getError
      }
    }
  }
</script>
<style lang='scss'>

  .cart-view{
    $root: &;
    .item-car .detail h3{
      font-size: 1em;
    }
    &__error{
      position: fixed;
      top: 0;
      right: 0;
      z-index: 20;
      transition: 0.4s ease all;
      color:white;
      background: hsl(0, 100%, 50%);
      width: 300px;
      padding: 15px 10px;
      text-align: center;
      h4{
        font-size: 1.2em;
      }
    }
    &__overlay{
      background: rgba(0,0,0,0.5);
      position: fixed;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      z-index: 10;
      transition: 0.4s ease all;
    }
    .box-caritem{
      transition: 0.4s ease all;
    }
    &--inactive{
      .box-caritem{
        right: -2500px;
      }
      #{$root}__overlay{
          background: transparent;
          z-index: -1;
        }
    }
  }
</style>