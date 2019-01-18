<template>
  <v-touch class="full-width full-height"
           @swipe2="getsureHandler"
           @swipe3="getsureHandler">
    <div class="fixed-center text-center">
      <p>
        <img
          src="~assets/sad.svg"
          style="width:30vw;max-width:150px;"
        >
      </p>
      <p class="text-faded">Sorry, nothing here...<strong>(404)</strong></p>
      <q-btn
        color="secondary"
        style="width:200px;"
        @click="$router.go(-1)">Go back</q-btn>
    </div>
  </v-touch>
</template>

<script>
export default {
  methods: {
    getsureHandler () { // 手势跳转
      this.$router.go(-1)
    }
  }
}
</script>
