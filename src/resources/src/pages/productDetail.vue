<template>
    <div class="row">
        <div class="col-md-6">
          <div class="wrap-gallery boxw">
            <div class="gallery-principal">
              <div class="product-image" v-if='productDetail.product_image'>
                <img :src="productDetail.product_image[0].image_big" alt=""/>
              </div>
            </div>
            <div class="gallery-thumb">
              <ul>
                <li v-for="image in productDetail.product_image"><a href=""><img :src="image.image" alt=""/></a></li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="detail-product">
            <div class="marca">{{productClass.product_class.influencer_name}}</div>
            <h2 class="title">{{productClass.product_class.name}}</h2>
            <div class="detalle-precio">
              <div class="price-promo">

                Precio: <span class="price">S/ {{productDetail.price}}</span>
              </div>
            </div>
            <div  :class="[attr.type_name === 'SELECT_SINGLE' ?  'cnt-size' : 'cnt-color']" v-for='attr in productClass.attributes'>
              <span class="text">{{attr.name_store}}:</span>
              <ul v-if="attr.type_name === 'SELECT_SINGLE'">
                <li v-for='option in attr.attribute_options_query'>
                  <a href="#">
                    <span>{{option.option}}</span>
                  </a>
                </li>
              </ul>
              <ul v-else>
                <li v-for='option in attr.attribute_options_query'>
                  <a href="#" class="">
                    <span :style='{background: option.attr}' ></span>
                  </a>
                </li>
              </ul>
            </div>
            <div class="cnt-color"><span class="text">Color:</span>

            </div>
            <div class="disponibilidad">
              <div class="counter-prin">
                <div class="cnt-quantity">
                  <div class="quantity-control">
                    <a class="menos" @click.prevent='quantityMenos'><i class="fa fa-minus"></i></a>
                    <input class="select-number" :value='productCart.quantity'/><a class="menos" @click.prevent='quantityMas'><i class="fa fa-plus"></i></a>
                  </div>
                </div>
                <div class="cnt-btn"><a @click.prevent='purchase()' class="btn btn-primary btn-compra">Comprar</a></div>
              </div>
            </div>
          </div>
        </div>
      </div>
</template>
<script>
  export default {
    name: 'productDetail',
    data () {
      return {
        productClass: {
          product_class: {
            influencer_name: ''
          }
        },
        productDetail: {

        },
        productCart: {
          quantity: 1,
          sku: ''
        }
      }
    },
    created () {
      this.getProduct()
      this.getProductDetail()
    },
    methods: {
      getProduct() {
        const self = this
        this.axios({
          method: 'get',
          url: '/api/product/' + this.$route.params.slug + '/',
          params: {
            'fields!': 'product_variant'
          }
        }).then(response => {
          self.productClass = response.data
        }).catch(error => {

        })
      },
      getProductDetail() {
        const self = this
        this.axios({
          method: 'get',
          url: '/api/product-detail/' + this.$route.params.slug + '/'
        }).then(response => {
          self.productDetail = response.data.product_variant
          self.productCart.sku = response.data.product_variant.sku
        }).catch(error => {

        })
      },
      quantityMenos() {
        if (this.productCart.quantity > 1) {
          this.productCart.quantity = this.productCart.quantity - 1
        }
      },
      quantityMas() {
        if (this.productDetail.stock > this.productCart.quantity) {
          this.productCart.quantity = this.productCart.quantity + 1
        }
      },
      purchase () {
        this.$store.dispatch('purchase', {
          sku: this.productCart.sku,
          quantity: this.productCart.quantity
        })
      }
    }
  }
</script>
<style lang='scss'>
  .quantity-control{
    a{
      cursor: pointer;
    }
  }
</style>