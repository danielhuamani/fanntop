<template>
    <div  v-else  class="col-md-9 product-list-mask">
    <div class="content">
      <div class="content-filter-top"></div>
      <div class="result">
        <div class="row">
          <div class="result-paginator result-paginator-top">
            <div class="order">
              <div class="text">Orden</div>
              <select>
                <option>todos</option>
                <option>Ascendente</option>
                <option>Descendente</option>
              </select>
            </div>
            <div class="paginator">
              <span class="item disabled">
                <i class="fa fa-angle-double-left"></i>
              </span>
              <span class="item disabled">
                <i class="fa fa-angle-left"></i>
              </span>
              <div class="text"></div>
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
          <div class="col-md-4"  v-for='product in productsMask' >
            <a href='' class="box item-result">
              <div class="image"> <img src=""/></div>
              <div class="detail">
                <h3 class="title"></h3>
                <!-- <h4 class="subtitle">subtitle</h4> -->
                <div class="price">
                  <span class="offer"></span>
                  <!-- <span class="normal tachado">S/. 80.15 PEN</span> -->
                </div>
              </div>
              <div class="fav"><span ><i class="fa fa-heart"></i></span></div>
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
  export default {
    name: 'productListFavoritesMask',
    data () {
      return {
        productsMask: [1,2,3,4,5,6,7,8,9,10,11,12]
      }
    }
  }
</script>