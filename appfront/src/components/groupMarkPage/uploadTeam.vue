<template>
  <el-upload
    class="upload-demo"
    :action="this.url+this.uploadUrl"
    :data="this.data"
    :before-upload="this.beforeUpload"
    :on-success="onSuccess">
    <el-button size="medium" type="primary">上传小组评分</el-button>
  </el-upload>
</template>

<script>
import axios from "axios"
export default {
  name: "uploadTeam",
  props: ["teamNo","teamScores"],
  data() {
    return {
      url:'',
      uploadUrl:'/teacher_api/upload_team',
      data:{key:this.teamNo[0]
        ,}
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
          if(res.data.teamScores){
            for(let i=0 ; i<res.data.teamScores.length;i++){
              this.$set(this.teamScores,i,res.data.teamScores[i])
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
