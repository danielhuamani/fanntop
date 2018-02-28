import Vue from 'vue'
import Router from 'vue-router'
import categoryList from '@/pages/categoryList'
import productDetail from '@/pages/productDetail'
// import cartView from '@/common/cartView'
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/categoria/:slug_parent_category/:slug_category/',
      name: 'category_list',
      component: categoryList
    },
    {
      path: '/producto/:slug/',
      name: 'product_detail',
      component: productDetail
    }
  ]
})
