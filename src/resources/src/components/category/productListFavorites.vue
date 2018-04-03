<template>
  <div class="col-md-12">
      <div class="result">
        <div class="row">
            <div class="col-md-12">
                <h3>Mis Favoritos</h3>
            </div>
        </div>
        <div class="row" v-if='products.results.length > 0'>
            <div class="col-md-3 col-sm-4 col-xs-6 col-mv"   v-for='product in products.results' >
                <a :href='"/producto/" + product.slug' class="box item-result">
                  <div class="image"> <img :src="product.product_variant.product_image.image"/></div>
                  <div class="detail">
                    <h3 class="title">{{product.name}}</h3>
                    <!-- <h4 class="subtitle">subtitle</h4> -->
                    <div class="price">
                      <span class="offer">S/. {{product.product_variant.price}}</span>
                      <!-- <span class="normal tachado">S/. 80.15 PEN</span> -->
                    </div>
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
  </div>
</template>
<script>
  export default {
    name: 'productListFavorites',
    props: ['products'],
    data () {
      return {
        orderBy: 'name_asc'
      }
    },
    methods: {
    }
  }
</script>
<style>
.row-no-product{
    margin-top: 40px;
    height: 200px;
}
</style>