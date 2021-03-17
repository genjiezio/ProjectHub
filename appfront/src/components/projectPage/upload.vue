<template>
  <el-card class="box-card">
    <el-upload
      class="upload-demo"
      :data="this.data"
      :action="this.url+this.uploadUrl"
      :on-preview="handlePreview"
      :on-remove="handleRemove"
      :before-remove="beforeRemove"
      :on-success="onSuccess"
      multiple
      :file-list="this.fileList">
      <el-button size="small" type="primary">点击上传</el-button>
      <div slot="tip" class="el-upload__tip">历史上传信息</div>
    </el-upload>
  </el-card>

</template>

<script>
import axios from "axios";

export default {
  props:["fileList","teamNo"],
  data(){
    return{
      url:'http://127.0.0.1:8000',
      uploadUrl:'/student_api/file_upload',
      data:{
        studentId:this.$route.query.qsid,
        groupId:this.$route.params.gid
      }
    }
  },
  methods: {
    handleRemove(file, fileList) {
      let index=-1
      if(fileList){
        for(let i=0;i<fileList.length;i++){
          if(file.name===fileList[i].name){
            index=i
          }
        }
      }

      axios.post("/student_api/file_delete", {
        fileId:index,
        key:this.$route.params.gid,
        studentId:this.$route.query.qsid
      },{
        headers: {
          "X-CSRFToken": document.cookie.split("=")[1],
        }}).then((res)=>{
        this.$message(res.data.status+":"+res.data.msg)
      })
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log("fileName:"+file.name)
      console.log("fileList:"+this.fileList)
      console.log("fileId:")
      let fileId = -1
      console.log("before change:"+fileId)
      if(this.fileList){
        for(let i=0;i<this.fileList.length;i++){
          if (this.fileList[i].name===file.name){
            fileId=this.fileList[i].id
          }
        }
      }
      console.log("after change:"+fileId)
      if (fileId===-1){
        alert("The document is not name")
      }
      else {
        console.log("before trans:"+fileId)
        axios({
          methods: "get",
          url:"/student_api/file_download",
          params:{
            groupId:this.$route.params.gid,
            fileId:fileId,
            studentId:this.$route.query.qsid,
          },
          responseType:"blob"
        }).then(res => {
          let blob = new Blob([res.data
          ]);
          let downloadElement = document.createElement("a");
          let href = window.URL.createObjectURL(blob); //创建下载的链接
          downloadElement.href = href;
          downloadElement.download = file.name; //下载后文件名
          document.body.appendChild(downloadElement);
          downloadElement.click(); //点击下载
          document.body.removeChild(downloadElement); //下载完成移除元素
          window.URL.revokeObjectURL(href); //释放掉blob对象
        })
      }
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${ file.name }？`);
    },
    onSuccess(response,file,fileList){
      this.$message(response.status+":"+response.msg)
      if(response.status===200){
        axios.get("/student_api/project_page",{params:{
            groupId:this.$route.params.gid,
            teacherId:this.$route.query.qtid,
            studentId:this.$route.query.qsid,
          }}).then((res)=>{
            this.fileList=res.data.fileList
        })
      }
    },
  }
}
</script>
