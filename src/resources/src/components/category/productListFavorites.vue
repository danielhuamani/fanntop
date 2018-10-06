<template>
  <div class="col-md-12">
      <div class="result">
        <div class="row">
            <div class="col-md-12">
                <h3 class='title_page'>Mis Favoritos</h3>
            </div>
        </div>
        <div class="result page-product__row_list__result" v-if='products.results.length > 0'>
          <div class="page-product__row_list__result__item page-product__row_list__result__item--4"  v-for='product in products.results' >
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
            </a>
          </div>
        </div>
        <div class="row row-no-product"  v-else >

            <div class="col-md-12">
                No tiene Productos Favoritos
            </div>

        </div>
      </div>
      <productDetailModal v-if='productSlug' @closeModal='closeModal' :productSlug='productSlug'></productDetailModal>
  </div>
</template>
<script>
  import productDetailModal from '@/components/category/productDetailModal'
  export default {
    name: 'productListFavorites',
    props: ['products'],
    components: {
      productDetailModal
    },
    data () {
      return {
        orderBy: 'name_asc',
        productSlug: ''
      }
    },
    methods: {
      closeModal () {
        this.productSlug = ''
      }
    }
  }
</script>
<style>
.row-no-product{
    margin-top: 40px;
    height: 200px;
}
</style>