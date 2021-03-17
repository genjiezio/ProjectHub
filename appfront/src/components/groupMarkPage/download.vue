<template>
  <div id="download" style="line-height: 10px">
    <el-card>
      <div slot="header" class="clearfix">
        <span style="font-weight: bold; font-size: 20px" >项目文件</span>
      </div>
      <el-form >
        <el-form-item v-for="(file,index) in fileList" :key="file[1]" style="height: 10px">
          <el-link @click="load(file[0],file[1])" icon="el-icon-document">{{file[0]}}</el-link>
        </el-form-item>
      </el-form>
    </el-card>

  </div>
</template>

<script>
import axios from "axios"
export default {
  name: "download",
  props:["fileList"],
  methods:{
    load(name,key){
      axios({
        methods: "get",
        url:"/teacher_api/get_file",
        params:{
          fileId:key
        },
        responseType:"blob"
      }).then(res => {
        let blob = new Blob([res.data]);
        let downloadElement = document.createElement("a");
        let href = window.URL.createObjectURL(blob); //创建下载的链接
        downloadElement.href = href;
        downloadElement.download = name; //下载后文件名
        document.body.appendChild(downloadElement);
        downloadElement.click(); //点击下载
        document.body.removeChild(downloadElement); //下载完成移除元素
        window.URL.revokeObjectURL(href); //释放掉blob对象
      })
    },
  }
}
</script>

<style scoped>

</style>
