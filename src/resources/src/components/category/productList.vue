<template>
  <div class="page-product__row_list__products">
    <div class="content">
      <div class="content-filter-switch">
        <div class="is_filter content-switch content-switch--product">
          <h4>Filtros</h4>
          <label class="switch">
            <input type="checkbox"  :checked='isFilter' @change='filterChange'>
            <span class="slider round"></span>
          </label>
        </div>
      </div>
      <div class="page-product__row_list__products__filter_top">
        <div class="page-product__row_list__products__search">
          <input type="text" class='form-control' @keyup='searchKey($event)' v-model='search'>
          <i class='far fa-search'></i>
        </div>
        <div class="page-product__row_list__products__order">
          <div class="text">Ordenar </div>
          <select v-model='orderBy' class='form-control' @change='changeOrderBy($event.target.value)'>
            <option value='name_asc'>Nombre (A-Z)</option>
            <option value='name_desc'>Nombre (Z-A)</option>
            <option value='price_asc'>Menor Precio</option>
            <option value='price_desc'>Mayor Precio</option>
          </select>
        </div>
      </div>
      <div class="result page-product__row_list__result" v-if='products.results.length > 0'>
        <div class="page-product__row_list__result__item"  v-for='product in products.results' >
          <a :href='"/producto/" + product.slug' class=" item-result">
            <div class="image"> <img :src="product.product_variant.product_image.image"/></div>
            <div class="page-product__row_list__result__item__name_price">
              <div class="detail">
                <h3 class="title">{{product.name}}</h3>
                <div class="price">
                  <span class="offer">S/. {{product.price}}</span>
                </div>
              </div>
              <i class='far fa-search' @click.prevent='productSlug = product.slug' ></i>
            </div>
            <div class="fav product_favorite" @click.prevent='addFavorite(product.id)'><span ><i class="fa fa-heart"></i></span></div>
          </a>
        </div>
      </div>
      <div class="row mt-20" v-else>
        <h2 class='notfound'>No se encontraron productos</h2>
      </div>
  <!--       <div class="row">
          <div class="result-paginator result-paginator-top">
            <div class="paginator"><span class="item disabled"><i class="fa fa-angle-double-left"></i></span><span class="item disabled"><i class="fa fa-angle-left"></i></span>
              <div class="text">1 De 8</div><a href="#" class="item"><i class="fa fa-angle-right"></i></a><a href="#" class="item"><i class="fa fa-angle-double-right"></i></a>
            </div>
          </div>
        </div> -->

    </div>
    <productDetailModal v-if='productSlug' @closeModal='closeModal' :productSlug='productSlug'></productDetailModal>
  </div>
</template>
<style>
  .notfound{
    margin-top: 30px;
  }
</style>
<script>
  import productDetailModal from '@/components/category/productDetailModal'
  import productItem from '@/components/category/productItem'
  export default {
    name: 'productList',
    props: ['products', 'isFilter'],
    data () {
      return {
        orderBy: 'name_asc',
        search: '',
        productSlug: '',
        isSetFilter: false
      }
    },
    components: {
      productItem,
      productDetailModal
    },
    methods: {
      isChecked () {
        return this.isFilter
      },
      filterChange () {
        this.$emit('filter', true)
      },
      closeModal () {
        this.productSlug = ''
      },
      changeOrderBy (value) {
        this.orderBy = value
        this.$emit('orderBy', this.orderBy)
      },
      searchKey (e) {
        this.$emit('search', this.search)
      },
      addFavorite (idProduct) {
        console.log(idProduct, 'idProduct')
        const self = this
        this.axios({
          method: 'post',
          url: '/api/product-favorite/',
          data: {
            product_id: idProduct
          }
        }).then(response => {

        }).catch(error => {

        })
      }
    }
  }
</script>