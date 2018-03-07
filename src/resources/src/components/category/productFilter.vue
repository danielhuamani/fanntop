<template>
  <div class="col-md-3" v-cloak>
    <div class="sidebar sidebar-filter box">
      <div class="w-filter" v-if="productsFilters.influencers">
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
                <i class="fa fa-check"> </i>
              </span>{{options.option}}
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
