<template>
  <div class="page-product__row_list__filter" v-cloak>
    <div class="sidebar sidebar-filter ">
      <h3 class="page-product__row_list__filter__title">FILTROS <i class="fas fa-list-ul"></i></h3>
      <div class="w-filter" v-if="productsFilters.influencers">
        <h3>Influencer </h3>
        <ul>
          <li>
            <label for="influencer_all">
              <input type="checkbox" value="todos" id="influencer_all"/><span class="filtros-check"> <i class="fa fa-check">  </i></span>Todos
            </label>
          </li>
          <li v-for='influencer_tag in productsFilters.influencers' :key='influencer_tag.id'>
            <label :for="influencer_tag.id">
              <input type="checkbox" :value="influencer_tag.slug" @change='changeInfluencer' v-model='influencer' :id="influencer_tag.id"/><span class="filtros-check"> <i class="fa fa-check">  </i></span>{{influencer_tag.name}}
            </label>
          </li>

        </ul>
      </div>
      <div class="w-filter" v-for="attribute in productsFilters.attributes" >
        <h3>{{attribute.name_store}}</h3>
        <ul class="colors" v-if="attribute.type_name === 'COLOUR'">

          <li :for="options.slug" v-for="options in attribute.attribute_options_query" :key='"color" + options.id'>
            <label >
              <input type="checkbox" :value="options.slug" @change='changeAttribute' v-model='attribute_option[attribute.slug]' :id="options.slug"/>
                <span class="filtros-check " :style="{ background: options.attr }">
              </span>
            </label>
          </li>
        </ul>
        <ul class="" v-if="attribute.type_name === 'SELECT_SINGLE'">
          <li v-for='options in attribute.attribute_options_query' :key='"select" + options.id'>
            <label :for="options.id">
              <input type="checkbox" :value="options.slug" @change='changeAttribute' v-model='attribute_option[attribute.slug]' :id="options.id"/>
              <span class="filtros-check">
                {{options.option}}
              </span>
            </label>
          </li>
        </ul>
      </div>
      <div class="w-filter">
        <h3>Precio</h3>
        <div class="w-filter__content">
          <vue-slider ref="slider" :tooltip-dir='tooltipDir'
          :min='productsFilters.prices[0]' :clickable='false' :tooltipStyle='tooltipStyle' v-on:drag-start='dragStart' v-on:drag-end='dragEnd' :max='productsFilters.prices[1]' :processStyle='processStyle' v-model="value"></vue-slider>
          <br>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import vueSlider from 'vue-slider-component'
  export default {
    name: 'productFilter',
    props: ['productsFilters', 'query'],
    components: {
      vueSlider
    },
    data () {
      return {
        influencer: [],
        attribute_option: {},
        prices: [],
        value: [
          0,
          2
        ],
        processStyle: {
          "backgroundColor": "#666666"
        },
        tooltipStyle: [
          {
            "backgroundColor": "#666666",
            "borderColor": "#666666",
          },
          {
            "backgroundColor": "#666666",
            "borderColor":"#666666",
          }
        ],
        tooltipDir: [
          "bottom",
          "bottom"
        ]
      }
    },
    created () {
      const self = this
      for(let attribute in self.productsFilters.attributes) {
        self.attribute_option[self.productsFilters.attributes[attribute]['slug']] = []
      }
      if (this.query['influencer']) {
        this.influencer = this.query['influencer']
      }
      if (this.query['attr']) {
        for(let attr in this.query['attr']) {
          let attr_slug = this.query['attr'][attr]
          self.attribute_option[attr_slug] = this.query[attr_slug]
        }
      }
      this.value = this.productsFilters.prices
      // for(let attr in )

    },
    methods: {
      changeInfluencer () {
        this.$emit('queryInfluencer', this.influencer)
      },
      changeAttribute () {
        this.$emit('queryAttribute', this.attribute_option)

      },
      dragStart (values) {
        this.$emit('valueStart', values.value)
      },
      dragEnd (values) {
        this.$emit('valueStart', values.value)
      }
    }
  }
</script>
