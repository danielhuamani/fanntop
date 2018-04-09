<template>
    <section class="main">
      <div class="container">

        <div class="row">
          <productListFavorites v-if="load_products" :products='products'></productListFavorites>
          <!--<productList v-if="products.results.length > 0" :products='products'></productList>-->
          <div  v-else-if='!load_products'  class="col-md-12 product-list-mask">
            <div class="content">
              <div class="content-filter-top"></div>
              <div class="result">
                <div class="row">
                  <div class="col-md-3 col-sm-4 col-xs-6 col-mv"  v-for='product in productsMask' >
                    <a href='' class="box item-result">
                      <div class="image"> <img src=""/></div>
                      <div class="detail">
                        <h3 class="title"></h3>
                        <!-- <h4 class="subtitle">subtitle</h4> -->
                        <div class="price">
                          <span class="offer"></span>
                          <!-- <span class="normal tachado">S/. 80.15 PEN</span> -->
                        </div>
                      </div>
                    </a>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
</template>
<script>
  import productFilterMask from '@/components/category/productFilterMask'
  import productFilter from '@/components/category/productFilter'
  import productListFavorites from '@/components/category/productListFavorites'
  import productListMask from '@/components/category/productListMask'
  export default {
    name: 'categoryList',
    data () {
      return {
        products: {
          results: []
        },
        productsFilters: {},
        query: {
          orderBy: 'name_asc'
        },
        prices: [],
        productsMask: [1,2,3],
        load_products: false,
        load_product_filter: false,
        load: false
      }
    },
    components: {
      productListFavorites,
      productFilter,
      productFilterMask
    },
    created () {
      this.getProducts()
    },
    methods: {
      getProducts (params) {
        const self = this
        this.axios({
          method: 'get',
          url: '/api/product-favorite/',
        }).then(response => {
          self.products = response.data
          self.load_products = true
        }).catch(error => {
          self.load_products = true
        })
      },
    }
  }
  // v-if='Object.keys(productsFilters).length > 0'
</script>
<style lang="scss">
  .product-list-mask{
    .title{
      height: 60px;
    }
  }
</style>