<template>
  <div class="col-md-9">
    <div class="content">
      <div class="content-filter-top"></div>
      <div class="result">
        <div class="row">
          <div class="result-paginator result-paginator-top">
            <div class="order">
              <div class="text">Ordenar por</div>
              <select v-model='orderBy' @change='changeOrderBy($event.target.value)'>
                <option value='name_asc'>Nombre (A-Z)</option>
                <option value='name_desc'>Nombre (Z-A)</option>
                <option value='price_asc'>Menor Precio</option>
                <option value='price_desc'>Mayor Precio</option>
              </select>
            </div>
            <div class="paginator">
              <span class="item disabled">
                <i class="fa fa-angle-double-left"></i>
              </span>
              <span class="item disabled">
                <i class="fa fa-angle-left"></i>
              </span>
              <div class="text">{{products.current_page}} De {{products.total_pages}}</div>
              <a href="#" class="item">
                <i class="fa fa-angle-right"></i>
              </a>
              <a href="#" class="item">
                <i class="fa fa-angle-double-right"></i>
              </a>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-4"  v-for='product in products.results' >
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
              <div class="fav"><span href="http://www.google.com.pe"><i class="fa fa-heart"></i></span></div>
            </a>
          </div>
        </div>
        <div class="row">
          <div class="result-paginator result-paginator-top">
            <div class="paginator"><span class="item disabled"><i class="fa fa-angle-double-left"></i></span><span class="item disabled"><i class="fa fa-angle-left"></i></span>
              <div class="text">1 De 8</div><a href="#" class="item"><i class="fa fa-angle-right"></i></a><a href="#" class="item"><i class="fa fa-angle-double-right"></i></a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import productItem from '@/components/category/productItem'
  export default {
    name: 'productList',
    props: ['products'],
    data () {
      return {
        orderBy: 'name_asc'
      }
    },
    components: {
      productItem
    },
    methods: {
      changeOrderBy (value) {
        console.log(value, 'value')
        this.orderBy = value
        this.$emit('orderBy', this.orderBy)
      }
    }
  }
</script>