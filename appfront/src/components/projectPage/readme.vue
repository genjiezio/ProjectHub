<template>
  <div id="readme">
<!--    <el-button type="primary" @click="showPdf()">主要按钮</el-button>-->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span style="font-size: 28px;font-weight: bold">README</span>
      </div>
      <VueMarkdown :source="readme"></VueMarkdown>
    </el-card>

  </div>
</template>

<script>
import axios from "axios";
import VueMarkdown from "vue-markdown";

export default {
  name: "readme",
  props:['location'],
  components:{VueMarkdown},
  data() {
    return {
      //PDF预览
      viewVisible: false,
      pdfPage : 1,
      pageCount: 0,
      readme: this.md2html(require(`../../../${this.location[0]}.md`))
    }
  },
}
</script>

<style scoped>
</style>
