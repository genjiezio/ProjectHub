<template>
  <div id="information">
    <el-container class="all-background">
      <el-header style="text-align: left; font-size: 20px; color: #ffff">
        <el-row style="margin: auto 15%">
          <HeadLine></HeadLine>
        </el-row>
      </el-header>

      <el-main>
        <div class="main-class">
          <el-card class="top-card">
            <el-row>
              <el-col class="avator" :span="5">
                <el-avatar src="/static/avtor.png" :size="65"></el-avatar>
              </el-col>
              <el-col :span="16">
                <el-row style="height: 15px">{{ user.name }}</el-row>
                <el-row>
                  <ul style="float: left; padding: 0 0">
                    <li class="el-icon-paperclip">
                      <a> {{ user.grade }} </a>
                    </li>
                    &nbsp;
                    <li class="el-icon-message">
                      <a> {{ user.mail }} </a>
                    </li>
                  </ul>
                </el-row>
              </el-col>
              <el-col style="margin-top: 2%" :span="3">
                <el-button @click="toEditUser = true">编辑</el-button>
              </el-col>
              <el-dialog title="修改信息" :visible.sync="toEditUser">
                <el-form :model="user" :rules="rules" ref="user">
                  <el-form-item label="姓名" label-width="120px" prop="name">
                    <el-input v-model="user.name" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="年级" label-width="120px" prop="grade">
                    <el-select v-model="user.grade" placeholder="请选择年级">
                      <el-option label="2015" value="2015"></el-option>
                      <el-option label="2016" value="2016"></el-option>
                      <el-option label="2017" value="2017"></el-option>
                      <el-option label="2018" value="2018"></el-option>
                      <el-option label="2019" value="2019"></el-option>
                      <el-option label="2020" value="2020"></el-option>
                      <el-option label="2021" value="2021"></el-option>
                      <el-option label="2022" value="2022"></el-option>
                      <el-option label="2023" value="2023"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="邮箱" label-width="120px" prop="mail">
                    <el-input v-model="user.mail" autocomplete="off"></el-input>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="canelEditUser">取 消</el-button>
                  <el-button @click="resetForm('user')">重置</el-button>
                  <el-button type="primary" @click="editUserDo('user')">确 定</el-button>
                </div>
              </el-dialog>
            </el-row>
          </el-card>
          <el-card class="mid-card">
            <el-tabs tab-position="left" v-model="activeName">
              <el-tab-pane name="1">
                <span slot="label"><i class="el-icon-user"></i>基本资料</span>
                <Basic v-bind:user="user" v-bind:query="this.query"> </Basic>
              </el-tab-pane>
              <el-tab-pane name="2">
                <span slot="label"><i class="el-icon-collection"></i>掌握技能</span>
                <Skill v-bind:query="this.query"></Skill>
              </el-tab-pane>
              <el-tab-pane name="3">
                <span slot="label"><i class="el-icon-folder"></i>参与项目</span>
                <Project v-bind:query="this.query"></Project>
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </div>
      </el-main>
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
  import Basic from "./Basic";
  import Skill from "./Skill";
  import Project from "./Project";

  export default {
    name: "information",
    components: {
      pageEnd,
      HeadLine,
      Basic,
      Skill,
      Project
    },
    data() {
      return {
        activeName: this.$route.query.aname ? this.$route.query.aname : "1",
        user: {
          name: "",
          grade: "",
          mail: "",
        },
        edit_user: {
          name: "",
          grade: "",
          mail: "",
        },
        toEditUser: false,
        rules: {
          name: [{
            required: true,
            message: "请输入姓名",
            trigger: "blur"
          }],
          grade: [{
            required: true,
            message: "请选择年级",
            trigger: "change"
          }],
          mail: [{
            required: true,
            message: "请填写邮箱",
            trigger: "blur"
          }],
        },
        query: this.$route.query.qsid,
      };
    },
    created() {
      axios
        .post("/student_api/get_info_user", {
          sid: this.$route.params.sid
        }, {
          headers: {
            "X-CSRFToken": document.cookie.split("=")[1],
          },
        })
        .then((res) => {
          this.user = res.data.user;
        });
      this.edit_user = this.user;
    },
    methods: {
      canelEditUser() {
        this.toEditUser = false;
        this.user = this.edit_user;
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      editUserDo(formName) {
        if (this.query !== undefined) {
          this.toEditUser = false;
          this.$message("你为什么想改别人的信息？");
          return;
        }
        this.$refs[formName].validate((valid) => {
          if (valid) {
            axios
              .post(
                "/student_api/edit_user", {
                  sid: this.$route.params.sid,
                  user: this.user,
                  basic: {
                    sex: "男",
                    edu: "本科",
                    school: "南方科技大学",
                    major: "CS",
                    desc: "垃圾",
                  },
                }, {
                  headers: {
                    "X-CSRFToken": document.cookie.split("=")[1],
                  },
                }
              )
              .then((res) => {
                if (res.data.status === 200) {
                  this.user = res.data.user;
                  this.edit_user = this.user;
                } else {
                  this.$message(res.data.msg);
                  this.user = this.edit_user;
                }
              });
            this.toEditUser = false;
            return true;
          } else {
            console.log("error submit!!");
            this.user = this.edit_user;
            this.toEditUser = false;
            return false;
          }
        });
      },
    },
  };
</script>

<style>
  .all-background {
    background-color: #f7f7f7;
    top: 0px;
    left: 0px;
    right: 0px;
    position: absolute;
    min-height: 120%;
  }

  .main-class {
    width: 70%;
    margin-left: 15%;
  }

  .el-header {
    background-color: #ffffff;
    line-height: 60px;
  }

  .el-footer {
    background-color: #ffffff;
    line-height: 20px;
  }

  #edit-button {
    float: right;
    display: inline-block;
  }

  .top-card {
    background-color: #ffffff;
    border-color: #f3f3f3;
  }

  .mid-card {
    background-color: #ffffff;
    border-color: #f3f3f3;
    margin-top: 2%;
    height: fit-content;
  }

  .content {
    margin-left: 3%;
    margin-right: 2%;
    margin-top: 2%;
  }

  .input-new-tag {
    width: 150px;
    margin-left: 2%;
    vertical-align: bottom;
  }

  .button-new-tag {
    margin-left: 2%;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }

  .avator {
    width: 80px;
    height: 80px;
  }

  .tag-cont {
    overflow: hidden;
    margin: 15px 0;
    display: block;
    zoom: 1;
  }

  .key-text {
    margin-left: 1%;
    font-size: 16px;
    color: #303133;
  }

  .value-text {
    font-size: 16px;
    text-align: right;
    color: #303133;
  }

  .main-class {
    width: 70%;
    margin-left: 15%;
  }

  .inline-block {
    display: inline-block;
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }

  .el-page-header__left {
    display: flex;
    cursor: pointer;
    margin-top: 20px;
    margin-right: 40px;
    position: relative;
  }

  .el-page-header__content {
    display: flex;
    cursor: pointer;
    font-size: 16px;
    color: #ffffff;
    margin-top: 20px;
    margin-right: 40px;
    position: relative;
  }
</style>
