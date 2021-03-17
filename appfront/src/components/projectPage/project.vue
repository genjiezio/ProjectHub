<template>
  <div id="project">
      <el-container class="all-background">
        <el-header style="text-align: left; font-size: 20px; color: #ffff">
          <el-row style="margin: auto 15%;" v-if="this.$route.query.qsid!==undefined">
            <HeadLine v-bind:id="studentId"></HeadLine>
          </el-row>
          <el-row style="margin: auto 15%;" v-if="this.$route.query.qtid!==undefined">
            <teacher-head-line v-bind:id="$route.query.qtid"></teacher-head-line>
          </el-row>
        </el-header>
        <el-container>
          <el-main>
            <el-card class="mid-card" style="margin: auto 20%;">
              <el-tabs tab-position="left">
                <el-tab-pane>
                  <span slot="label"><i class="el-icon-info"></i>基本资料</span>
                  <group-information
                  v-bind:project-name="projectName"
                  v-bind:group-id="groupId"
                  v-bind:leader-id="leaderId"
                  v-bind:members="members"
                  v-bind:class-name="className"
                  v-bind:group-name="groupName"
                  v-bind:student-id="studentId"
                  v-bind:personal-score="personalScore"
                  v-bind:group-score="groupScore"
                  v-bind:lab-name="labName"
                  ></group-information>
                </el-tab-pane>
                <el-tab-pane>
                  <span slot="label"><i class="el-icon-user"></i>组内成员</span>
                  <name-list
                    v-bind:members="members"
                    v-bind:student-id="studentId"
                    v-bind:group-id="groupId"
                    v-bind:leader-id="leaderId"
                    style="text-align: center"
                  ></name-list>
                </el-tab-pane>
                <el-tab-pane>
                  <span slot="label"><i class="el-icon-eleme"></i>上传文件</span>
                  <span v-if="SA">
                     <teacher-download
                       v-bind:file-list="fileList"
                     ></teacher-download>
                  </span>
                  <span v-else-if="this.$route.query.qsid!==undefined">
                    <upload
                      v-bind:file-list="fileList"
                      v-bind:team-no="groupId"></upload>
                  </span>
                  <span v-if="this.$route.query.qtid!==undefined" >
                    <teacher-download
                      v-bind:file-list="fileList"
                    ></teacher-download>
                  </span>
                </el-tab-pane>
                <el-tab-pane>
                  <span slot="label"><i class="el-icon-date"></i>答辩时间</span>
                  <presentation
                    v-bind:presentation="presentation"
                    v-bind:group-id="groupId"
                    v-bind:student-id="studentId"
                    v-bind:choose-time="chooseTime"
                    v-bind:s-a="SA"
                    style="text-align: center"></presentation>
                </el-tab-pane>
                <el-tab-pane>
                  <span slot="label"><i class="el-icon-document-copy"></i>日志信息</span>
                  <log
                    v-bind:logs="logs"
                  ></log>
                </el-tab-pane>
                <el-tab-pane>
                  <el-link slot="label" v-if="this.$route.query.qtid || SA" :href="jump()"><i class="el-icon-document-copy"></i>跳转评分</el-link>
                </el-tab-pane>
              </el-tabs>
            </el-card>
          </el-main>
        </el-container>
        <el-footer>
          <page-end></page-end>
        </el-footer>
      </el-container>
  </div>
</template>


<script>
import HeadLine from "../HeadLine";
import NameList from "./nameList";
import upload from "./upload";
import axios from "axios";
import pageEnd from "../pageEnd";
import presentation from "./presentation";
import groupInformation from "./groupInformation";
import log from "./log"
import TeacherHeadLine from "../TeacherHeadLine";
import teacherDownload from "./teacherDownload";
export default {
  name: 'project',
  components: {NameList, HeadLine,upload,pageEnd,presentation,groupInformation,log,TeacherHeadLine,teacherDownload},
  data(){
    return{
      groupId: this.$route.params.gid,
      studentId: this.$route.query.qsid,
      leaderId: 1,
      projectName:"",
      className:"",
      groupName:"",
      labName:"",
      groupScore:0,
      personalScore:0,
      members:[],
      fileList: [],
      presentation:[],
      chooseTime:[],
      logs:[],
      teamScores:[],
      SA:false,
      intervalId:null,
    }
  },
  created() {
    console.log(this.$route.params.gid)
    axios.get("/student_api/project_page",{params:{
        groupId:this.$route.params.gid,
        teacherId:this.$route.query.qtid,
        studentId:this.$route.query.qsid,
      }}).then((res)=>{
        if(res.data.status===200){
          this.members=res.data.members
          this.leaderId=res.data.leaderId
          this.fileList=res.data.fileList
          this.presentation=res.data.timeList
          this.className=res.data.className
          this.projectName=res.data.projectName
          this.logs=res.data.logs
          this.groupName=res.data.groupName
          this.chooseTime=res.data.chooseTime
          this.labName=res.data.labName
          this.SA=res.data.SA
          this.groupScore=res.data.groupScore
          this.personalScore=res.data.personalScore
        }
        else if(res.data.status===1001){
          this.$alert("您没有访问该小组权限",'',function(){
            let jump = document.createElement("a")
            jump.href = '/'+this.$route.query.qsid+'?qsid'+this.$route.query.qsid
            jump.click()
            document.body.removeChild(jump)
          });
        }
        else if(res.data.status===1002){
          this.$alert("您没有访问该小组权限",'',function(){
            let jump = document.createElement("a")
            jump.href = '/teacher/'+this.$route.query.qtid+'?qtid'+this.$route.query.qtid
            jump.click()
            document.body.removeChild(jump)
          });
        }
        else{
          this.$message(res.data.status+":"+res.data.msg)
        }
      }
    )
    this.dataRefresh()
  },
  methods:{
    jump(){
      if(this.SA){
        return '/groupMark/'+this.$route.params.gid+'?qsid='+this.$route.query.qsid
      }
      else {
        return '/groupMark/'+this.$route.params.gid+'?qtid='+this.$route.query.qtid
      }
    },
    dataRefresh() {
      // 计时器正在进行中，退出函数
      if (this.intervalId != null) {
        return;
      }
      // 计时器为空，操作
      this.intervalId = setInterval(() => {
        console.log("刷新" + new Date());
        axios.get("/student_api/project_page",{params:{
            groupId:this.$route.params.gid,
            teacherId:this.$route.params.qtid,
            studentId:this.$route.query.qsid,
          }}).then((res)=>{
            if(res.data.presentation){
              this.members=res.data.members
              this.leaderId=res.data.leaderId
              this.fileList=res.data.fileList
              this.presentation=res.data.timeList
              this.className=res.data.className
              this.projectName=res.data.projectName
              this.logs=res.data.logs
              this.groupName=res.data.groupName
              this.chooseTime=res.data.chooseTime
              this.labName=res.data.labName
              this.SA=res.data.SA
              this.groupScore=res.data.groupScore
              this.personalScore=res.data.personalScore
            }
          }
        )
      }, 5000);
    },
    // 停止定时器
    clear() {
      clearInterval(this.intervalId); //清除计时器
      this.intervalId = null; //设置为null
    },
  },
  destroyed(){
    // 在页面销毁后，清除计时器
    this.clear();
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
