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
  el: '#page',
  router,
  store,
  components: {
    cartView
  },
  delimiters: ['#{', '}'],
  data: {
    emailSuscription: '',
    showEmailSuscription: false,
    messageEmailSuscription: ''
  },
  methods: {
    changeStatusCartView () {
      this.$store.dispatch('changeStatusCartView', true, true)
    },
    submitSuscription () {
      const self = this
      this.axios.post('/api-suscripcion/', {
        email: self.emailSuscription,
      })
      .then(function (response) {
        self.showEmailSuscription = true
        self.emailSuscription = ''
        self.messageEmailSuscription = 'Gracias por suscribirte'
      })
      .catch(function (error) {
        self.emailSuscription = ''
        self.messageEmailSuscription = error.response.data.email[0]
      });
    }
  }
})
