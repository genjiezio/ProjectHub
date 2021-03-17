<template>
  <el-upload
    class="upload-demo"
    :action="this.url+this.uploadUrl"
    :data="this.data"
    :on-success="onSuccess"
  >
    <el-button size="medium" type="primary">上传个人评分</el-button>
  </el-upload>
</template>

<script>
import axios from "axios"
export default {
  name: "uploadPersonal",
  props: ["teamNo","personalScore"],
  data() {
    return {
      url:'',
      uploadUrl:'/teacher_api/upload_person',
      data:{key:this.teamNo[0],}
    };
  },
  created() {
    this.url="http://127.0.0.1:8000"
  },
  methods: {
    onSuccess(response,file,fileList){
      alert(response.status+":"+response.msg)
      if (response.status===200){
        axios.get("/teacher_api/group_mark",{params:{id:this.$route.params.gid}}).then((res)=>{
          if(res.data.personalScore){
            for(let i=0 ; i<res.data.personalScore.length;i++){
              this.$set(this.personalScore,i,res.data.personalScore[i])
            }
          }
        })
      }
    },
  }
}
</script>

<style scoped>
</style>
