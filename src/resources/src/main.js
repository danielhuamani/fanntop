import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import cartView from '@/components/common/cartView'
import VueAxios from 'vue-axios'
import store from './vuex'
import VueCookie from 'vue-cookie'

Vue.use(VueAxios, axios)
Vue.use(VueCookie)
Vue.axios.defaults.headers.common['cookiename'] = 'csrftoken';
Vue.axios.defaults.headers.common['X-CSRFToken'] = Vue.cookie.get('csrftoken');
Vue.axios.defaults.headers.common['Accept'] = 'application/json';
Vue.axios.defaults.headers.common['credentials'] = 'same-origin';
Vue.axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
new Vue({
  el: '#app',
  router,
  store,
  components: {
    cartView
  },
  methods: {
    changeStatusCartView () {
      this.$store.dispatch('changeStatusCartView', true, true)
    }
  }
})
