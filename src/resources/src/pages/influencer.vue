<template>
    <section class="main page-product">
      <div class="content">
        <div class="page-product__row_list">
          <productFilter :query='query' @valueStart='valueStart' @valueEnd='valueEnd' :isFilter='isFilter' @changeFilter='changeSetFilter()'
          @queryInfluencer='queryInfluencer' @queryAttribute='queryAttribute'
          :productsFilters='productsFilters' v-if='load_product_filter'></productFilter>
          <productList :isFilter='isFilter' v-on:orderBy='orderBy' v-on:search='search' v-if="load_products" @filter='filter' :products='products'></productList>
        </div>
<!--
        <div class="row">
          <div class="col-md-3">
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
                        <h4 class="subtitle">subtitle</h4>
                        <div class="price">
                          <span class="offer"></span>
                          <span class="normal tachado">S/. 80.15 PEN</span>
                        </div>
                      </div>
                      <div class="fav"><span ><i class="fa fa-heart"></i></span></div>
                    </a>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div> -->
      </div>
    </section>
</template>
<script>
  import productFilterMask from '@/components/category/productFilterMask'
  import productFilter from '@/components/category/productFilter'
  import productList from '@/components/category/productList'
  import productListMask from '@/components/category/productListMask'
  export default {
    name: 'influencerList',
    data () {
      return {
        products: {
          results: []
        },
        productsFilters: {},
        query: {
          orderBy: 'name_asc',
          search: ''
        },
        productsMask: [1,2,3],
        load_products: false,
        load_product_filter: false,
        isFilter: false
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
      this.query['orderBy'] = 'name_asc'
      this.getProducts(this.query)
      this.getProductsFilters(this.query)
    },
    methods: {
      filter (value) {
        this.isFilter = value
      },
      changeSetFilter () {
        this.isFilter = false
      },
      search (value) {
        this.query['search'] = value
        this.setRouter(this.query)
        this.getProducts(this.query)
      },
      orderBy (order) {
        this.query['orderBy'] = order
        this.setRouter(this.query)
        this.getProducts(this.query)
      },
      getProducts (params) {
        const self = this
        this.axios({
          method: 'get',
          url: '/api/product-influencer/' + this.$route.params.slug + '/',
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
          url: '/api/influencer-filter/' + this.$route.params.slug + '/',
          params: params
        }).then(response => {
          self.productsFilters = response.data
          self.load_product_filter = true
        }).catch(error => {

        })
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
  .content-filter-switch{
    display:none;
  }
  @media screen and (max-width: 1000px) {
    .content-filter-switch{
      display:block;
    }
  }
</style>