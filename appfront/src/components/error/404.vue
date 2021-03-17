<template>
  <div class="wscn-http404">
    <div class="pic-404">
      <img class="pic-404__parent" src="@/assets/404.png" />
    </div>
    <div style="display: inline-block">
      <div class="oops">OOPS!</div>
      <div class="headline">{{ message }}</div>
      <div class="info">Please check that the URL you entered is correct.</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Page404",
  computed: {
    message() {
      return "The webmaster said that you can not enter this page...";
    },
  },
};
</script>

<style scoped>
.wscn-http404 {
  position: absolute;
  top: 10%;
  left: 25%;
}
.oops {
  font-size: 32px;
  font-weight: bold;
  line-height: 40px;
  color: #1482f0;
  margin-bottom: 20px;
}
.headline {
  font-size: 20px;
  line-height: 24px;
  color: #222;
  font-weight: bold;
  margin-bottom: 10px;
}
.info {
  font-size: 13px;
  line-height: 21px;
  color: grey;
  margin-bottom: 30px;
}
</style>
