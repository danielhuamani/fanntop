import Vue from 'vue'
import Vuex from 'vuex'
import moduleCartView from './cartView'
Vue.use(Vuex)
const store = new Vuex.Store({
  modules: {
    moduleCartView: moduleCartView
  }
})

export default store
