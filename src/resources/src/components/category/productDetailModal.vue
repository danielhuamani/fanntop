<template>
    <div class="modal  modal product_detail_modal fade in"  tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" @click='closeModal'>
      <div class="row product_detail_vue product_detail_modal-dialog modal-dialog" @click.stop>
       <div class="product_detail_modal__close" @click='closeModal'>
          <i class='far fa-times'></i>
      </div>
       <div class="product_detail_vue__content">
          <div class="detail-product text-center">
            <h2 class="title">{{productClass.product_class.name}}</h2>
            <div class="detalle-precio detalle-precio--modal">
              <div class="price">
                Precio: <span class="price">S/ {{productDetail.price}}</span>
              </div>
            </div>
          </div>
            <div class="wrap-gallery ">
              <div class="gallery-principal">
                <div class="product-image" v-if='productDetail.product_image'>
                  <img  :src="productDetail.product_image[indexPager].image_small" alt=""/>
                </div>
                <div class="product-image_pagers">
                  <div class="product-image_pagers__item" :class="{ 'product-image_pagers__item--active': index == indexPager }" v-for="(image, index) in productDetail.product_image" @click='indexPager = index'>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
            <div class="product_detail_modal__filter_purchase">
              <div class="w-filter product_detail_modal__w-filter">
                <div  :class="[attr.type_name === 'SELECT_SINGLE' ?  'cnt-size' : 'cnt-color']" v-for='attr in productClass.attributes'>
                  <span class="text">{{attr.name_store}}:</span>
                  <ul v-if="attr.type_name === 'SELECT_SINGLE'" class='sizes'>
                    <li v-for='option in attr.attribute_options_query'>
                      <label :for="option.slug">
                        <input type="radio" v-model='selectProduct[attr.slug]'  :value="option.slug" @change='changeSize' :id="option.slug" :name="attr.slug"/>
                        <span class="filtros-check">{{option.option}}
                        </span>
                      </label>
                    </li>
                  </ul>
                  <ul v-else class='colors'>
                    <li v-for='option in attr.attribute_options_query'
                     >
                      <label :for="option.slug">
                        <input type="radio" v-model='selectProduct[attr.slug]' :value="option.slug" @change='changeColor' :id="option.slug" :name="attr.slug"/>
                          <span class="filtros-check" :style='{background: option.attr}' ></span>
                      </label>

                    </li>
                  </ul>
                </div>

              </div>
              <div class="product_detail_modal__disponibilidad disponibilidad" v-if='!isExhausted'>
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
              <div v-else class="disponibilidad product_detail_modal__disponibilidad">
                <button class="btn btn-dark">
                  Agotado
                </button>
              </div>
            </div>

        </div>
      </div>
  </div>
</template>
<script>
  export default {
    name: 'productDetailModal',
    props: ['productSlug'],
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
        },
        stockMaximo: 0,
        selectProduct: {
          attr: []
        },
        changeColorAttr: false,
        select_length: '',
        isExhausted: false,
        indexPager: 0
      }
    },
    created () {
      this.getProduct()
      this.getProductDetail()
    },
    methods: {
      closeModal () {
        this.$emit('closeModal')
      },
      getProduct() {
        const self = this
        this.axios({
          method: 'get',
          url: '/api/product/' + this.productSlug + '/',
          params: {
            'fields!': 'product_variant'
          }
        }).then(response => {
          self.productClass = response.data
        }).catch(error => {

        })
      },
      isActiveProductDetail (attr, attrType) {
        var is_active = false
        console.log('is active', attr, attrType)
        if (this.selectProduct[attrType]) {
          if (this.selectProduct[attrType] === attr) {
            return true
          }
        }

        return is_active
      },
      verifyProductDetail () {
        const self = this
        var product_class = self.productClass.product_class.product_class_products
        var productDetail = {}
        for (var index in product_class) {
          var status = []
          for (var new_index in product_class[index]['attribute_option']) {
            for(var select_index in self.selectProduct) {
              if (self.selectProduct[select_index] === product_class[index]['attribute_option'][new_index].slug) {
                status.push(true)
                // break
              }
            }
          }
          if (status.length === self.select_length) {
            productDetail = product_class[index]
          }

        }
        return productDetail
      },
      changeSize () {
        // console.log(slugAttr, slugType)
        // if (this.selectProduct[slugType] === slugAttr) {
        //   console.log('entro')
        // } else {
        //   this.$set(this.selectProduct, slugType, slugAttr)
        // }
        const self = this
        let resultVerify = this.verifyProductDetail()
        console.log(resultVerify, '----')
        self.productCart['quantity'] = 1
        if (resultVerify['sku']){
          if (!resultVerify['is_exhausted']) {
            self.isExhausted = resultVerify['is_exhausted']
            self.productCart['sku'] = resultVerify['sku']
            self.stockMaximo = resultVerify['stock']
            if (self.changeColorAttr) {
              self.getProductDetail()
            }
          } else {
            self.isExhausted = true
            self.productCart['sku'] = ''
            self.stockMaximo = 0
          }
        } else {
          self.isExhausted = true
          self.productCart['sku'] = ''
          self.stockMaximo = 0
        }
      },
      changeColor () {
        // if (this.selectProduct[slugType] === slugAttr) {
        //   console.log('entro')
        // } else {
        //   this.$set(this.selectProduct, slugType, slugAttr)
        // }
        const self = this
        let resultVerify = this.verifyProductDetail()
        self.changeColorAttr = true
        self.productCart['quantity'] = 1
        if (resultVerify['sku']){
          if (!resultVerify['is_exhausted']) {
            self.isExhausted = resultVerify['is_exhausted']
            self.productCart['sku'] = resultVerify['sku']
            self.stockMaximo = resultVerify['stock']
            self.getProductDetail()
          } else {
            self.isExhausted = true
            self.productCart['sku'] = ''
            self.stockMaximo = 0
          }
        } else {
          self.isExhausted = true
          self.productCart['sku'] = ''
          self.stockMaximo = 0
        }
      },
      getProductDetail() {
        const self = this
        this.axios({
          method: 'get',
          url: '/api/product-detail/' + this.productSlug + '/',
          params: self.selectProduct
        }).then(response => {
          self.productDetail = response.data
          self.productCart.sku = response.data.sku
          self.stockMaximo = response.data.stock
          self.isExhausted = response.data.is_exhausted
          self.select_length = self.productDetail.attribute_option.length
          self.selectProduct['attr'] = []
          self.changeColorAttr = false
          for(var index in self.productDetail.attribute_option) {
            self.selectProduct[self.productDetail.attribute_option[index].attribute_name] = self.productDetail.attribute_option[index].slug
            self.selectProduct['attr'].push(self.productDetail.attribute_option[index].attribute_name)
          }
        }).catch(error => {

        })
      },
      quantityMenos() {
        if (this.productCart.quantity > 1) {
          this.productCart.quantity = this.productCart.quantity - 1
        }
      },
      quantityMas() {
        if (this.stockMaximo > this.productCart.quantity) {
          this.productCart.quantity = this.productCart.quantity + 1
        }
      },
      purchase () {
        this.$store.dispatch('purchase', {
          sku: this.productCart.sku,
          quantity: this.productCart.quantity
        })
        this.$emit('closeModal')
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
  .product_detail_modal{
    display: block !important;
    background: rgba(0,0,0, 0.7);
    ::-webkit-scrollbar {
        width: 7px;
    }

    /* Track */
    ::-webkit-scrollbar-track {
        box-shadow: inset 0 0 5px grey;
        border-radius: 6px;
    }

    /* Handle */
    ::-webkit-scrollbar-thumb {
        background: grey;
        border-radius: 6px;
    }

    /* Handle on hover */
    ::-webkit-scrollbar-thumb:hover {
        background: #000000;
    }

    &__filter_purchase{
      padding: 0 10px;
      display: flex;
    }
    .btn-compra{
      margin: 0;
      padding: 0 20px;
      height: 52px;
      line-height: 52px;
      font-size: 14px;
    }
    &__w-filter{
      margin: 0;
      padding: 0;
      border-bottom: none;
      width: calc(100% - 230px);
    }
    &__disponibilidad{
      width: 230px;
      .counter-prin{
        display: flex;
        align-items: center;
      }
    }
  }
  .product_detail_modal-dialog{
    padding: 20px 0;
    border-radius: 8px;
    background: white;
    overflow-y: scroll;
    height: calc(100vh - 50px);

  }
  .product_detail_modal__close{
    position: absolute;
    top: -2px;
    right: 5px;
    font-size: 24px;
    cursor: pointer;
  }
  @media (max-width: 480px){
    .product_detail_modal-dialog{
      height: calc(100vh - 100px);
    }
    .product_detail_modal{
      .btn-compra{
        height: 38px;
        line-height: 40px;
      }
      &__filter_purchase{
        flex-direction: column;
        margin-bottom: 10px;
      }
      &__disponibilidad{
        width: 100%;
      }
      &__w-filter{
        width: 100%;
      }
    }
  }
</style>