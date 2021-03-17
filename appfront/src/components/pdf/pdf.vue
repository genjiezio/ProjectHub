<template>
  <div id = "container" :class = "{'back': isShow}" >
    <canvas id = "the-canvas" >
    </canvas>
    <!-- / / 添加关闭pdf功能-->

    <span :class = "{'close':isShow}" :hidden="!isShow" @click = "closePdf" ><i class="el-icon-close" style="font-size: 40px"></i></span>
      <p class="foot" v-if="pdfDoc">
        <Button class="left" :hidden="!isShow"  @click="onPrevPage" v-if="pageNum>1">上一页</Button >
        <Button class = "right" :hidden="!isShow"  @click = "onNextPage" v-if = "pageNum < pdfDoc.numPages" > 下一页 </Button>
      </p >
  </div>
</template>

<script>
import PDFJS from 'pdfjs-dist'
export default {
  name: "pdf",
  data(){
    return{
      isShow:false,
      pdfDoc:null,
      pageNum:1,
      pageRendering: false,
      pageNumPending: null,
      scale:0.9
    }
  },
  methods:{
    closePdf() {
      this.isShow = false
    },
    showPDF(url){
      this.isShow = true
      let _this = this
      PDFJS.getDocument(url).promise.then(
        function(pdf){
          _this.pdfDoc = pdf
          _this.renderPage(1)
        })
    },
    renderPage(num){
      this.pageRendering= true
      let _this=this
      this.pdfDoc.getPage(num).then(
        function (page){
          var viewport = page.getViewport(_this.scale)
          let canvas = document.getElementById('the-canvas')
          canvas.height = viewport.height
          canvas.width = viewport.width
          var renderContext = {
            canvasContext: canvas.getContext('2d'),
            viewport: viewport
          }
          var renderTask = page.render(renderContext)
          renderTask.promise.then(function(){
            _this.pageRendering=false
            if (_this.pageNumPending !== null) {
              // New page rendering is pending
              this.renderPage(_this.pageNumPending)
              _this.pageNumPending = null
            }
          })
        }
      )
    },
    queueRenderPage(num){
      if(this.pageRendering){
        this.pageNumPending=num
      }
      else {
        this.renderPage(num)
      }
    },
    onPrevPage() {
      if (this.pageNum <= 1) {
        return
      }
      this.pageNum--
      this.queueRenderPage(this.pageNum)
    },
    onNextPage() {
      if (this.pageNum >= this.pdfDoc.numPages) {
        return
      }
      this.pageNum++
      this.queueRenderPage(this.pageNum)
    }

  }
}
</script>

<style scoped="" type="text/css">
.back {
  background-color: rgba(0, 0, 0, 0.788); position:fixed;
  width: 100%;
  height: 100%;
  top: 0; left: 0;
  text-align: center;
  padding: 20px;
  z-index: 100;
  overflow: scroll;
}
.close{
  position: absolute;
  right: 20px;
  top: 20px;
  z-index: 200;
  color: #fff;
  cursor: pointer;
}
.foot {
  position: absolute;
  bottom: 50px;
  left: 50%;
  transform: translate(-50%,0);
}
</style>
