<template>
  <div id="nameList">
    <el-card class="box-card" :key="key">
      <div slot="header" class="clearfix">
        <el-row>
          <el-col span="12" style="text-align: left">
            <span style="font-weight: bold; font-size: 20px;">成员列表</span>
          </el-col>
          <el-col span="8" push="4">
            <span :hidden=" parseInt(leaderId) !== parseInt(studentId)">
              <el-button type="danger" @click="deleteGroup">移除小组</el-button>
            </span>
          </el-col>
        </el-row>
      </div>
      <div v-for="member in members" class="text item">
        <el-row style="line-height: 10px">
          <el-col span="4" push="1">
            <el-avatar :src="member.picture"></el-avatar>
          </el-col>
          <el-col span="8">
            <br>
              <el-link :href="link(member)" target="_self"
                       :underline="false" style="font-size: 20px">
              {{member.name}}
            </el-link>


          </el-col>
          <el-col span="8" push="4">
            <span :hidden="(parseInt(studentId))!==(parseInt(member.studentId))">
              <el-button type="danger"
                         @click="deleteStu(member)">退出小组</el-button>
            </span>
          </el-col>
        </el-row>
        <el-divider></el-divider>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "nameList",
  props: ["members", "studentId", "groupId", "leaderId"],
  data() {
    return {
      mem: {
        picture: "",
        name: "",
        studentId: -1
      },
      Size: "medium",
      fit: "contain",
      key: 0,
    }
  },
  methods: {
    deleteStu() {
      let find = -1

      if (this.members) {
        for (let i = 0; i < this.members.length; i++) {
          if (parseInt(this.members[i].studentId) === parseInt(this.studentId)) {
            find = i;
            break;
          }
        }
      }
      console.log(find)

      console.log(this.members)
      axios.post("/student_api/member_delete",
        {
          groupKey: this.$route.params.gid,
          studentKey: this.$route.query.qsid
        },{
          headers: {
            "X-CSRFToken": document.cookie.split("=")[1],
          }}).then((res) => {
          if (res.data.status) {
            if (res.data.status === 200) {
              let jump = document.createElement("a")
              jump.href = '/' + this.$route.query.qsid + '?qsid=' + this.$route.query.qsid
              jump.click()
              document.body.removeChild(jump)
              if (find > -1) {
                this.members.splice(find, 1)
              }
            } else {
              this.$message(res.data.status + ":" + res.data.msg)
            }
          }
        }
      )
      this.key++
    },
    deleteGroup() {
      axios.post("/student_api/group_delete",
        {
          groupKey: this.$route.params.gid,
          studentKey: this.$route.query.qsid
        },{
          headers: {
            "X-CSRFToken": document.cookie.split("=")[1],
          }}).then((res) => {
          if (res.data.status) {
            if (res.data.status === 200) {
              let jump = document.createElement("a")
              jump.href = '/' + this.$route.query.qsid + '?qsid=' + this.$route.query.qsid
              jump.click()
              document.body.removeChild(jump)
            } else {
              this.$message(res.data.status + ":" + res.data.msg)
            }
          }
        }
      )
    },
    link(member){
      if(this.$route.query.qsid!==undefined){
        return '/'+member.studentId+'/information?aname=1&qsid='+this.studentId
      }
      else if(this.$route.query.qtid!==undefined){
        return '/'+member.studentId+'/information?aname=1&qtid='+this.$route.query.qtid
      }
      return ''
    }
  }
}
</script>

<style scoped>

</style>
