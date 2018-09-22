<template>
    <div class="home_influencer__search" :class='{"home_influencer__search--active": influencerList.length > 0}'>
      <input type="text" class='home_influencer__search__input' v-on:keyup="getInfluencer($event)">
      <i class='far fa-search home_influencer__search__icon' ></i>
      <div class="home_influencer__search__api" v-if='influencerList.length > 0'>
          <a class="home_influencer__search__api__influencer" v-for='inf in influencerList'>
                <img :src="inf.image_crop" class='home_influencer__search__api__influencer__img' width="" height="">
                <h3 class='home_influencer__search__api__influencer__name'>{{inf.name}}</h3>
          </a>

      </div>
    </div>
</template>
<script>
    export default {
        name: 'Home',
        data () {
            return {
                influencerList: []
            }
        },
        methods: {
            getInfluencer (e) {
                const self = this
                if (e.target.value) {
                    this.axios({
                      method: 'get',
                      url: '/api/influencer-list/',
                      params: {
                        'search': e.target.value
                      }
                    }).then(response => {
                      self.influencerList = response.data
                    }).catch(error => {
                    })
                } else {
                    this.influencerList = []
                }
            }
        }

    }
</script>