<template>
    <section class="main">
      <div class="container">

        <div class="row">
          <productFilter :query='query' @queryInfluencer='queryInfluencer' @queryAttribute='queryAttribute'
          :productsFilters='productsFilters' v-if='Object.keys(productsFilters).length > 0'></productFilter>
          <productList :products='products'></productList>
        </div>
      </div>
    </section>
</template>
<script>
  import productFilter from '@/components/category/productFilter'
  import productList from '@/components/category/productList'
  export default {
    name: 'categoryList',
    data () {
      return {
        products: [],
        productsFilters: {},
        query: {}
      }
    },
    components: {
      productList,
      productFilter
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
      getProducts (params) {
        const self = this
        this.axios({
          method: 'get',
          url: '/api/product-category/' + this.$route.params.slug_parent_category + '/' + this.$route.params.slug_category + '/',
          params: params
        }).then(response => {
          self.products = response.data
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
</script>