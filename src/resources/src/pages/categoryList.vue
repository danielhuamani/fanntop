<template>
    <section class="main">
      <div class="container">

        <div class="row">
          <productFilter :query='query' @valueStart='valueStart' @valueEnd='valueEnd' @queryInfluencer='queryInfluencer' @queryAttribute='queryAttribute'
          :productsFilters='productsFilters' v-if='load_product_filter'></productFilter>
          <div class="col-md-3" v-else>
            <div class="sidebar sidebar-filter box">
              <div class="w-filter">
                <h3></h3>
                <ul>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>
                  <li>
                    <label for="influencer_all">
                      <p class='mask'></p>
                    </label>
                  </li>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>

                </ul>
              </div>
              <div class="w-filter">
                <h3></h3>
                <ul>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>
                </ul>
              </div>
              <div class="w-filter">
                <h3></h3>
                <ul>
                  <li>
                    <label for="influencer_all">
                      <p class="mask"></p>
                    </label>
                  </li>
                </ul>
              </div>

            </div>
          </div>
          <productList v-if="load_products" v-on:orderBy='orderBy' :products='products'></productList>
          <!--<productList v-if="products.results.length > 0" :products='products'></productList>-->
          <div  v-else  class="col-md-9 product-list-mask">
            <div class="content">
              <div class="content-filter-top"></div>
              <div class="result">
                <div class="row">
                  <div class="result-paginator result-paginator-top">
                    <div class="order">
                      <div class="text">Orden</div>
                      <select>
                        <option>todos</option>
                        <option>Ascendente</option>
                        <option>Descendente</option>
                      </select>
                    </div>
                    <div class="paginator">
                      <span class="item disabled">
                        <i class="fa fa-angle-double-left"></i>
                      </span>
                      <span class="item disabled">
                        <i class="fa fa-angle-left"></i>
                      </span>
                      <div class="text"></div>
                      <a href="#" class="item">
                        <i class="fa fa-angle-right"></i>
                      </a>
                      <a href="#" class="item">
                        <i class="fa fa-angle-double-right"></i>
                      </a>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4"  v-for='product in productsMask' >
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
                      <div class="fav"><span ><i class="fa fa-heart"></i></span></div>
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
  import productList from '@/components/category/productList'
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
        load_product_filter: false
      }
    },
    components: {
      productList,
      productFilter,
      productFilterMask
    },
    created () {
      // let attr = this.$route.query['attr']
      // for(let q in this.$route.query) {
      //   this.$set(this.query, q, this.$route.query[q])
      // }
      // this.setQuery(this.$route.query)
      if (typeof(this.$route.query.influencer) === 'string') {
        this.query['influencer'] = [this.$route.query.influencer]
      } else {
        if (this.$route.query.influencer) {
          this.query['influencer'] = this.$route.query.influencer
        }
      }

      if (typeof(this.$route.query.attr) === 'string') {
        this.query['attr'] = [this.$route.query.attr]
      } else {
        if (this.$route.query.attr) {
          this.query['attr'] = this.$route.query.attr
        }
      }
      for(let attr in this.query['attr']){
        let attr_slug = this.query['attr'][attr]
        this.query[attr_slug] = this.$route.query[attr_slug]
        if (typeof(this.query[attr_slug]) === 'string') {
          this.query[attr_slug] = [this.$route.query[attr_slug]]
        } else {
          if (this.$route.query.attr) {
            this.query[attr_slug] = this.$route.query[attr_slug]
          }
        }
      }

      this.getProducts(this.query)
      this.getProductsFilters(this.query)
    },
    methods: {
      orderBy (order) {

        this.query['orderBy'] = order
        this.setRouter(this.query)
        this.getProducts(this.query)
      },
      valueEnd (prices) {
        this.prices = prices
        this.query['prices'] = prices
        this.setRouter(this.query)
        this.getProducts(this.query)
      },
      valueStart (prices) {
        this.prices = prices
        this.query['prices'] = prices
        this.setRouter(this.query)
        this.getProducts(this.query)
      },
      getProducts (params) {
        const self = this
        this.axios({
          method: 'get',
          url: '/api/product-category/' + this.$route.params.slug_parent_category + '/' + this.$route.params.slug_category + '/',
          params: params
        }).then(response => {
          self.products = response.data
          self.load_products = true
        }).catch(error => {

        })
      },
      getProductsFilters(params) {
        const self = this
        this.axios({
          method: 'get',
          url: '/api/category-filter/' + this.$route.params.slug_parent_category + '/' + this.$route.params.slug_category + '/',
          params: params
        }).then(response => {
          self.productsFilters = response.data
          self.load_product_filter = true
        }).catch(error => {

        })
      },
      setRouter (query) {
        this.$router.push({query: query})
      },
      setQuery (query) {
        this.query = query
      },
      queryInfluencer (influencerFIlter) {
        this.query['influencer'] = influencerFIlter
        this.setRouter(this.query)
        this.getProducts(this.query)
        this.getProductsFilters(this.query)
        // this.$set(this.query, 'influencer', influencerFIlter)
      },
      queryAttribute (attributeFilter) {
        this.query['attr'] = []
        for(let attribute in attributeFilter) {
          if (attributeFilter[attribute].length) {
            if (this.query['attr'].length > 0) {
              this.query['attr'].push(attribute)
            } else {
              this.query['attr'] = []
              // this.query[attribute] = []
              this.query['attr'].push(attribute)
              // this.query[attribute].push()
            }
            // if (this.query[attribute]) {
            //   this.query[attribute]
            // } else {
            //   this.query[attribute] = {}
            // }
            this.$set(this.query, attribute, attributeFilter[attribute])
          } else {
            this.$delete(this.query, attribute)
          }
        }
        if (this.query['attr'].length === 0) {
          this.$delete(this.query, 'attribute')
        }
        this.setRouter(this.query)
        this.getProducts(this.query)
      }
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