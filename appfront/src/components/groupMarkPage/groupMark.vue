<template>
  <div id="groupMark">
    <el-container class="all-background">
      <el-header style="text-align: left; font-size: 20px; color: #ffff">
        <el-row style="margin: auto 15%;" v-if="studentId!==undefined">
          <HeadLine v-bind:id="studentId"></HeadLine>
        </el-row>
        <el-row style="margin: auto 15%;" v-else>
          <TeacherHeadLine v-bind:id="teacherId"></TeacherHeadLine>
        </el-row>
      </el-header>
      <el-container>
        <el-main >
          <team-score
            v-bind:team-score="teamScores"></team-score>
          <total-score
            v-bind:team-scores="teamScores"
            v-bind:team-score="teamScore"></total-score>
          <br>
          <download
            v-bind:file-list="fileList"></download>
        </el-main>
        <el-aside width="30%">
          <el-row >
            <el-col span=23>
              <br>
              <personal-score
                v-bind:personal-score="personalScore"
                v-bind:team-score="teamScore"></personal-score>
            </el-col>
          </el-row>
          <br>
          <el-row style="text-align: center">
            <el-col span="12">
              <upload-team
                v-bind:team-no="teamNo"
                v-bind:team-scores="teamScores"></upload-team>
            </el-col>
            <el-col span="12">
              <upload-personal
                v-bind:team-no="teamNo"
                v-bind:personal-score="personalScore">
              </upload-personal>
            </el-col>
          </el-row>
        </el-aside>
      </el-container>
      <el-footer>
        <page-end></page-end>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
import HeadLine from "../HeadLine";
import pageEnd from "../pageEnd";
import TeamScore from "./teamScore";
import TotalScore from "./totalScore";
import PersonalScore from "./personalScore";
import uploadTeam from "./uploadTeam";
import uploadPersonal from "./uploadPersonal";
import download from "./download";
import TeacherHeadLine from "../TeacherHeadLine";
export default {
  name: 'groupMark',
  components: {PersonalScore, TotalScore, TeamScore, HeadLine,pageEnd,uploadTeam,uploadPersonal,download,TeacherHeadLine},
  data(){
    return{
      teacherId:this.$route.query.qtid,
      studentId:this.$route.query.qsid,
      teamScores:[
      ],
      personalScore:[

      ],
      teamScore: [0],
      teamNo: [this.$route.params.gid],
      fileList:[
        
      ]
    }
  },
  created() {
    console.log(this.studentId)
    axios.get("/teacher_api/group_mark",{params:{
        teacherId:this.$route.query.qtid,
        studentId:this.$route.query.qsid,
        id:this.$route.params.gid}}).then((res)=>{
          if(res.data.status===200){
            this.teamScores=res.data.teamScores
            this.personalScore=res.data.personalScore
            this.fileList=res.data.fileList
          }
          else {
            if(this.$route.query.qtid!==undefined){
              this.$alert("您无权限访问",'',function(){
                let jump = document.createElement("a")
                jump.href = '/teacher/'+this.$route.query.qtid+'?qtid'+this.$route.query.qtid
                jump.click()
                document.body.removeChild(jump)
              })
            }
            else if(this.$route.query.qsid!==undefined){
              this.$alert("您没有访问该小组权限",'',function(){
                let jump = document.createElement("a")
                jump.href = '/'+this.$route.query.qsid+'?qsid'+this.$route.query.qsid
                jump.click()
                document.body.removeChild(jump)
              });
            }
          }
        })
  },
}
</script>
<style>
.all-background {
  background-color: #f7f7f7;
  top: 0px;
  left: 0px;
  right: 0px;
  position: absolute;
  min-height: 110%;
}
.el-header {
  background-color: #ffffff;
  line-height: 60px;
}

.el-footer {
  background-color: #ffffff;
  line-height: 20px;
}

</style>
