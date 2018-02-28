<template>
  <div class="col-md-4"><a href="#" class="box item-result">
    <div class="image"> <img :src="product.product_variant.product_image.image"/></div>
    <div class="detail">
      <h3 class="title">{{product.name}}</h3>
      <!-- <h4 class="subtitle">subtitle</h4> -->
      <div class="price">
        <span class="offer">S/. {{product.product_variant.price}}</span>
        <!-- <span class="normal tachado">S/. 80.15 PEN</span> -->
      </div>
    </div>
    <div class="fav"><span href="http://www.google.com.pe"><i class="fa fa-heart"></i></span></div></a>
  </div>
</template>
<script>
  export default {
    name: 'productItem',
    props: ['product']
  }
</script>