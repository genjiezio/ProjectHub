<template>
  <div id="groupInformation">
    <div class="content">
      <el-row>
        <span style="display: inline-block; font-size: 28px">基本资料</span>
      </el-row>
      <el-divider></el-divider>
      <el-form label-width="20%" >
        <el-form-item label="所选项目" >
          <span >{{ projectName }}</span>
        </el-form-item>
        <el-form-item label="所属课程" >
          <span >{{ className }}</span>
        </el-form-item>
        <el-form-item label="所属实验课" >
          <span >{{ labName }}</span>
        </el-form-item>
        <el-form-item label="组长姓名">
          <el-link href="https://www.csdn.net/" target="_self" :underline="false">
            <span style="font-size: 14px">{{this.findLeader()}}</span>
          </el-link>
        </el-form-item>
        <el-form-item label="小组名称">
          <el-row>
            <el-col span="12">
              {{groupName}}
            </el-col>
            <span :hidden="this.checkMember()">
            <el-col span="12">
              <el-button @click="vis = true">更改小组名称</el-button>
            </el-col>
            </span>
          </el-row>
        </el-form-item>
        <span :hidden="checkMember()">
          <el-form-item label="小组得分">
            {{groupScore}}
          </el-form-item>
          <el-form-item label="个人得分">
            {{personalScore}}
          </el-form-item>
        </span>
      </el-form>
      <el-dialog title="更改分数"
                 :visible.sync = vis
                 :before-close="handleClose"
                 style="text-align: center">
        <el-form>
          <el-form-item label="小组名称">
            <el-input
              v-model="name"
              placeholder="请输入小组名称"
            ></el-input>
          </el-form-item>
        </el-form>
        <el-button @click="vis = false">取 消</el-button>
        <el-button type="primary" @click="addDo">确 定</el-button>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "groupInformation",
  props:["projectName","groupId","members","leaderId","className","groupName","studentId","groupScore","personalScore","labName"],
  data(){
    return{
      leader:this.findLeader(),
      vis: false,
      name:undefined,
    }
  },
  methods:{
    findLeader(){
      if(this.members){
        for (let i = 0; i < this.members.length; i++) {
          if (parseInt(this.members[i].studentId) === this.leaderId)	{
            return this.members[i].name
          }
        }
      }
    },
    handleClose(done) {

      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
    },
    addDo(){
      console.log("start change")
      this.groupName=this.name
      this.vis = false;
      axios.post("/student_api/change_group_name",{
        groupId:this.$route.params.gid,
        groupName:this.groupName
      },{
        headers: {
          "X-CSRFToken": document.cookie.split("=")[1],
        }}).then((res)=>{})
    },
    checkMember(){
      if(this.members){
        for(let i=0;i<this.members.length;i++){
          console.log()
          if(this.members[i].studentId===parseInt(this.$route.query.qsid)){
            return false
          }
        }
      }
      return true
    }
  }
}
</script>

<style scoped>
</style>
