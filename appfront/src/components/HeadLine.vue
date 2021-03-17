<template xmlns:el-col="http://www.w3.org/1999/html">
  <div class="HeadLine">
    <el-row>
      <el-col :span="6" class="Title">
        <el-image style="width: 127px; height: 46px; margin-top: 7px" :src="logo_url"></el-image>
      </el-col>
      <el-col :span="2" :offset="5">
        <el-link :href="'/' + id" target="_self" :underline="false">主页</el-link>
      </el-col>
      <el-col :span="3" :offset="6" style="line-height: 18px">
        <br />
        <el-popover placement="bottom" width="450" trigger="click">
          <div style="max-height: 300px; overflow: auto">
            <el-card v-for="(msg, index) in msgs" :key="index" class="msg-card">
              <div slot="header">
                <el-col :span="5" style="font-size: 16px">{{
                  msg.sender
                }}</el-col>
                <el-col :span="5" style="font-size: 14px">{{
                  msg.project
                }}</el-col>
                <el-col :span="8" style="font-size: 12px">{{
                  msg.date
                }}</el-col>
                <el-button style="float: right; padding: 0px 0px" type="text" icon="el-icon-close" @click="deleteMsg(index)"></el-button>
                <el-button v-if="msg.needConfirm" style="float: right; padding: 0px 0px" type="text" @click="confirmMsg(index, false)">拒绝</el-button>
                <el-button v-if="msg.needConfirm" style="float: right; padding: 0px 0px" type="text" @click="confirmMsg(index, true)">同意</el-button>
              </div>
              <div>
                <span style="font-size: 14px">{{ msg.content }}</span>
              </div>
            </el-card>
          </div>
          <el-button @click="drawer = true" style="margin-left: 8px" size="small" icon="el-icon-message" slot="reference">
            消息
          </el-button>
        </el-popover>
      </el-col>
      <el-col :span="2" style="line-height: 10px">
        <br />
        <el-popover placement="bottom" width="300" trigger="hover">
          <el-row style="height: 15px">
            <el-col :span="6" class="inf">
              <br />
              Fancy UI
            </el-col>
          </el-row>
          <el-divider></el-divider>
          <el-row style="text-align: center">
            <el-col :span="8">
              <el-link :href="'/' + id + '/information?aname=1'" target="_self" :underline="false">
                <el-row>
                  <i class="el-icon-user" style="font-size: 36px"></i>
                </el-row>
                <el-row> 基本资料 </el-row>
              </el-link>
            </el-col>
            <el-col :span="8">
              <el-link :href="'/' + id + '/information?aname=2'" target="_self" :underline="false">
                <el-row>
                  <i class="el-icon-collection" style="font-size: 36px"></i>
                </el-row>
                <el-row> 掌握技能 </el-row>
              </el-link>
            </el-col>
            <el-col :span="8">
              <el-link :href="'/' + id + '/information?aname=3'" target="_self" :underline="false">
                <el-row>
                  <i class="el-icon-folder" style="font-size: 36px"></i>
                </el-row>
                <el-row> 参与项目 </el-row>
              </el-link>
            </el-col>
          </el-row>
          <el-divider style="line-height: 1px"></el-divider>
          <el-row style="text-align: center; margin-bottom: 2px">
            <el-col :span="12">
              <el-link href="/findpassword" target="_self" :underline="false">
                <i class="el-icon-setting" style="font-size: 15px">
                  修改密码
                </i>
              </el-link>
            </el-col>
            <el-col :span="12">
              <el-link href="/login" target="_self" :underline="false" @click="loginOut">
                <a class="el-icon-turn-off" style="font-size: 15px; float: center">
                  退出登录</a>
              </el-link>
            </el-col>
          </el-row>
          <el-avatar :src="fig" slot="reference"> </el-avatar>
        </el-popover>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import axios from "axios";
  export default {
    name: "Head",
    data() {
      return {
        logo_url: "/static/logo1.png",
        fig: "/static/avtor.png",
        drawer: false,
        msgs: [{
            mid: "",
            sender: "",
            date: "",
            needConfirm: false,
            content: "",
            project: "",
            accepted: false,
          },
        ],
        id: this.$route.query.qsid,
      };
    },
    created() {
      this.id = this.$route.query.qsid ?
        this.$route.query.qsid :
        this.$route.params.sid;
      console.log(this.id);
      axios.post("/student_api/get_message", {
        sid: this.id
      }, {
        headers: {
          "X-CSRFToken": document.cookie.split("=")[1],
        },
      }).then((res) => {
        this.msgs = res.data.msgs;
      });
    },
    methods: {
      confirmMsg(index, confirm) {
        this.msgs[index].needConfirm = false;
        //后端把该消息needConfirm -> false;
        axios
          .post(
            "/student_api/confirm_msg", {
              mid: this.msgs[index].mid,
              sid: this.id,
              accepted: confirm
            }, {
              headers: {
                "X-CSRFToken": document.cookie.split("=")[1],
              },
            }
          )
          .then((res) => {
            if (res.data.status === 200) {
              this.msgs[index].needConfirm = false;
            } else {
              this.$message(res.data.msg);
            }
          });
      },
      deleteMsg(index) {
        if (this.msgs[index].needConfirm) {
          this.$message("请确认后再删除");
          return;
        }
        axios
          .post(
            "/student_api/delete_msg", {
              mid: this.msgs[index].mid,
              sid: this.id
            }, {
              headers: {
                "X-CSRFToken": document.cookie.split("=")[1],
              },
            }
          )
          .then((res) => {
            this.msgs = res.data.msgs;
            this.$message(res.data.msg);
          });
      },
      loginOut() {
        axios
          .post(
            "/student_api/login_out", {
              sid: this.id
            }, {
              headers: {
                "X-CSRFToken": document.cookie.split("=")[1],
              },
            }
          )
          .then((res) => {});
      },
    },
  };
</script>

<style scoped>
  .all-background {
    background-color: #f3f3f3;
    top: 0px;
    left: 0px;
    right: 0px;
    position: absolute;
    min-height: 100%;
  }

  .msg-card {
    border-radius: 3px;
    background: #ffffff;
    margin: 1% auto;
    width: 98%;
  }

  .el-menu-demo {
    background-color: #f3f3f3;
  }

  .inf {
    text-align: -moz-left;
    font-size: 18px;
    line-height: 10px;
  }

  .el-popover {
    line-height: 1px;
  }

  .Title {
    color: white;
    font-size: 28px;
    text-align: left;
  }
</style>
