<template>
  <div id="basic">
    <div class="content">
      <el-row>
        <span style="display: inline-block; font-size: 28px">基本资料</span>
        <span>
          <el-button v-if="toEditBasic" id="edit-button" @click="BasicButton"
            >编辑</el-button
          >
          <el-button v-else id="edit-button" @click="BasicEditDone"
            >完成</el-button
          >
        </span>
      </el-row>
      <el-divider></el-divider>
      <el-form ref="infoBasic" :model="infoBasic" label-width="20%">
        <el-form-item label="我的性别">
          <span v-if="toEditBasic">{{ infoBasic.sex }}</span>
          <span v-else>
            <el-radio v-model="infoBasic.sex" label="男">男</el-radio>
            <el-radio v-model="infoBasic.sex" label="女">女</el-radio>
          </span>
        </el-form-item>
        <el-form-item label="我的学历">
          <span v-if="toEditBasic">{{ infoBasic.edu }}</span>
          <span v-else>
            <el-radio v-model="infoBasic.edu" label="本科">本科</el-radio>
            <el-radio v-model="infoBasic.edu" label="硕士">硕士</el-radio>
            <el-radio v-model="infoBasic.edu" label="博士">博士</el-radio>
          </span>
        </el-form-item>
        <el-form-item label="我的简介">
          <span v-if="toEditBasic">{{ infoBasic.desc }}</span>
          <span v-else>
            <el-input type="textarea" :rows="2" v-model="infoBasic.desc">
            </el-input>
          </span>
        </el-form-item>
        <el-form-item label="我的专业">
          <span v-if="toEditBasic">{{ infoBasic.major }}</span>
          <span v-else>
            <el-input v-model="infoBasic.major"></el-input>
          </span>
        </el-form-item>
        <el-form-item label="我的学校">
          <span v-if="toEditBasic">{{ infoBasic.school }}</span>
          <span v-else>
            <el-input v-model="infoBasic.school"></el-input>
          </span>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Basic",
  props: ["user", "query"],
  created() {
    axios
      .post("/student_api/get_info_user", { sid: this.$route.params.sid },{
        headers: {
          "X-CSRFToken": document.cookie.split("=")[1],
        },
      })
      .then((res) => {
        this.infoBasic = res.data.basic;
        this.user = res.data.user;
      });
  },
  data() {
    return {
      toEditBasic: true,
      infoBasic: {
        sex: "",
        edu: "",
        school: "",
        major: "",
        desc: "",
      },
    };
  },
  methods: {
    BasicButton() {
      if (this.query !== undefined) {
        alert("你为什么想改别人的信息？");
        return;
      }
      this.toEditBasic = false;
    },
    BasicEditDone() {
      console.log(this.$route.params.sid);
      this.toEditBasic = true;
      axios
        .post(
          "/student_api/edit_user",
          {
            sid: this.$route.params.sid,
            user: this.user,
            basic: this.infoBasic,
          },
          {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          }
        )
        .then((res) => {
          this.infoBasic = res.data.basic;
        });
    },
  },
};
</script>

<style>
.content {
  margin-left: 3%;
  margin-right: 2%;
  margin-top: 2%;
}
</style>
