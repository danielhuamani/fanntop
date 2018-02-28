<template>
  <div class="col-md-3">
    <div class="sidebar sidebar-filter box">
      <div class="w-filter">
        <h3>Influencer</h3>
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
      <div class="w-filter" v-for="attribute in productsFilters.attributes">
        <h3>{{attribute.name_store}}</h3>
        <ul class="colors" v-if="attribute.type_name === 'COLOUR'">
          <li v-for="options in attribute.attribute_options_query" :key='"color" + options.id'>
            <a href="#" >
              <span :style="{ background: options.attr }"></span>
            </a>
          </li>
        </ul>
        <ul class="" v-if="attribute.type_name === 'SELECT_SINGLE'">
          <li v-for='options in attribute.attribute_options_query' :key='"select" + options.id'>
            <label :for="options.id">
              <input type="checkbox" :value="options.slug" @change='changeAttribute' v-model='attribute_option[attribute.slug]' :id="options.id"/>
              <span class="filtros-check">
                <i class="fa fa-check"> </i>
              </span>{{options.option}}
            </label>
          </li>
          <li v-for="options in attribute.attribute_options_query" :key='options.id'><a href="#" > <span :style="{ background: options.attr }"></span></a></li>
        </ul>
      </div>
      <div class="w-filter">
        <h3>Ropa</h3>
        <ul>
          <li>
            <label for="todosropa">
              <input type="checkbox" value="todos" id="todosropa"/><span class="filtros-check"><i class="fa fa-check"> </i></span>Todos
            </label>
          </li>
          <li>
            <label for="casacas">
              <input type="checkbox" value="casacas" id="casacas"/><span class="filtros-check"><i class="fa fa-check"> </i></span>Casacas
            </label>
          </li>
          <li>
            <label for="poleras">
              <input type="checkbox" value="todos" id="poleras"/><span class="filtros-check"><i class="fa fa-check"> </i></span>Poleras
            </label>
          </li>
          <li>
            <label for="polos">
              <input type="checkbox" value="todos" id="polos"/><span class="filtros-check"><i class="fa fa-check"> </i></span>Polos
            </label>
          </li>
          <li>
            <label for="pantalones">
              <input type="checkbox" value="todos" id="pantalones"/><span class="filtros-check"><i class="fa fa-check"> </i></span>Pantalones
            </label>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'productFilter',
    props: ['productsFilters', 'query'],
    data () {
      return {
        influencer: [],
        attribute_option: {}
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
      // for(let attr in )

    },
    methods: {
      changeInfluencer () {
        this.$emit('queryInfluencer', this.influencer)
      },
      changeAttribute () {
        this.$emit('queryAttribute', this.attribute_option)

      }
    }
  }
</script>