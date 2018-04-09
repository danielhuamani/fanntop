import Vue from 'vue'
import Router from 'vue-router'
import categoryList from '@/pages/categoryList'
import influencer from '@/pages/influencer'
import influencerNew from '@/pages/influencerNew'
import productDetail from '@/pages/productDetail'
import productFavorites from '@/pages/productFavorites'
import cart from '@/pages/cart'
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
      path: '/mis-favoritos/',
      name: 'product_favorites',
      component: productFavorites
    },
    {
      path: '/producto/:slug/',
      name: 'product_detail',
      component: productDetail
    },
    {
      path: '/influenciador-new/:slug/',
      name: 'influencerNew',
      component: influencerNew
    },
    {
      path: '/influenciador/:slug/',
      name: 'influencer',
      component: influencer
    },
    {
      path: '/carro-compras/',
      name: 'cart',
      component: cart
    }
  ]
})
