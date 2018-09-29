import Vue from 'vue'

const moduleCartView = {
  state: {
    statusCartView: false,
    cart: {
      cart_items: [],
      extra_data: {
        msj: ''
      }
    },
    isMenu: false,
    error: ''
  },
  getters: {
    getStatusCartView: state => {
      return state.statusCartView
    },
    getCart: state => {
      return state.cart
    },
    getIsMenu: state => {
      return state.isMenu
    },
    getError: state => {
      return state.error
    }
  },
  mutations: {
    changeStatusCartView (state, status) {
      state.statusCartView = status
    },
    setCart (state, cart) {
      state.cart = cart
    },
    setIsMenu (state, status) {
      state.isMenu = status
    },
    setError (state, error) {
      state.error = error
    }
  },
  actions: {
    purchase ({commit}, product) {
      const self = this
      Vue.axios({
        method: 'post',
        url: '/api/cart/',
        data: product
      }).then(response => {
        console.log(product.notMenu, 'product.notMenu')
        if (!product.notMenu) {
          commit('changeStatusCartView', true)
          commit('setIsMenu', true)
        }
        commit('setCart', response.data)
      }).catch(error => {
        commit('setError', error.response.data.error)
        commit('setCart', error.response.data)
        setTimeout(()=> {
          commit('setError', '')
        }, 3000)
      })
    },
    deleteCartItem ({commit}, product) {
      const self = this
      Vue.axios({
        method: 'delete',
        url: '/api/cart/',
        data: product
      }).then(response => {
        if (!product.notMenu) {
          commit('changeStatusCartView', true)
          commit('setIsMenu', true)
        }
        commit('setCart', response.data)
      }).catch(error => {
        commit('setError', error.response.data.error)
        setTimeout(()=> {
          commit('setError', '')
        }, 3000)
      })
    },
    changeStatusCartView ({commit}, status, isMenu) {
      if (status) {
        if (isMenu) {
          if (this.getters.getIsMenu) {
            commit('changeStatusCartView', status)
          } else {
            Vue.axios.get('/api/cart/', {
            }).then(response => {
              commit('setCart', response.data)
              commit('changeStatusCartView', status)
              commit('setIsMenu', true)
            }).catch(e => {
              commit('changeStatusCartView', status)
            })
          }
        } else {
          Vue.axios.get('/api/cart/', {
          }).then(response => {
            commit('setCart', response.data)
            commit('changeStatusCartView', status)
            commit('setIsMenu', true)
          }).catch(e => {
            commit('changeStatusCartView', status)
          })
        }
      } else {
        commit('changeStatusCartView', status)
      }
    },
    getCartView ({commit}) {
      Vue.axios.get('/api/cart/', {
      }).then(response => {
        commit('setCart', response.data)
        commit('setIsMenu', true)
      }).catch(e => {
        // commit('changeStatusCartView', status)
      })
    }
  }
}

export default moduleCartView
