<template>
  <div class="login" clearfix>
    <div class="login-wrap">
      <el-row type="flex" justify="center">
        <el-form
          ref="loginForm"
          :model="user"
          :rules="rules"
          status-icon
          label-width="80px"
        >
          <h3>登录</h3>
          <hr />
          <el-form-item prop="username" label="用户名">
            <el-input
              v-model="user.username"
              placeholder="请输入用户名"
              prefix-icon
            ></el-input>
          </el-form-item>
          <el-form-item id="password" prop="password" label="密码">
            <el-input
              v-model="user.password"
              show-password
              placeholder="请输入密码"
            ></el-input>
          </el-form-item>
          <router-link to="/findpassword" class="left-right-link"
            >找回密码</router-link
          >
          <router-link to="/register" class="left-right-link"
            >注册账号</router-link
          >
          <br />
          <el-button type="primary" @click="doLogin()" class="inline-block"
            >学生登录</el-button
          >
          <el-button type="primary" @click="teaLogin()" class="inline-block"
            >教师登录</el-button
          >
        </el-form>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "login",
  data() {
    return {
      user: {
        username: "",
        password: "",
        csrf_token: "",
      },
    };
  },
  created() {
    axios.get("/padmin_api/get_csrf_token", {}).then((res) => {
      this.csrf_token = res.data.csrf_token;
    });
  },
  methods: {
    doLogin() {
      if (!this.user.username) {
        this.$message.error("请输入用户名！");
      } else if (!this.user.password) {
        this.$message.error("请输入密码！");
      } else {
        axios
          .post(
            "/student_api/check_account",
            {
              name: this.user.username,
              password: this.user.password,
            },
            {
              headers: {
                "X-CSRFToken": this.csrf_token,
              },
            }
          )
          .then((res) => {
            if (res.data.status === 200) {
              this.$router.push({
                name: "HomePage",
                params: { sid: res.data.sid },
              });
            } else if (res.data.status === 207) {
              alert("您账号已从另一设备下线");
              this.$router.push({
                name: "HomePage",
                params: { sid: res.data.sid },
              });
            } else {
              alert("密码错误！");
            }
          });
      }
    },
    teaLogin() {
      if (!this.user.username) {
        this.$message.error("请输入用户名！");
      } else if (!this.user.password) {
        this.$message.error("请输入密码！");
      } else {
        axios
          .post(
            "/teacher_api/check_account",
            {
              name: this.user.username,
              password: this.user.password,
              job: "T",
            },
            {
              headers: {
                "X-CSRFToken": this.csrf_token,
              },
            }
          )
          .then((res) => {
            if (res.data.status === 200) {
              this.$router.push({
                name: "ProManage",
                params: { tid: res.data.tid },
                query: {aname: "1"}
              });
            } else if (res.data.status === 207) {
              alert("您账号已从另一设备下线");
              this.$router.push({
                name: "ProManage",
                params: { tid: res.data.tid },
                query: {aname: "1"}
              });
            } else {
              alert("密码错误！");
            }
          });
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login {
  background: url("../assets/bg1.png") no-repeat center center;
  background-size: 100% 100%;
  top: 0px;
  left: 0px;
  right: 0px;
  bottom: 0px;
  position: absolute;
  overflow: hidden;
}

.login-wrap {
  width: 400px;
  height: 325px;
  margin: 12% auto;
  padding-top: 10px;
  line-height: 40px;
  border-radius: 5px;
  background: #ffffff;
}

#password {
  margin-bottom: 5px;
}

h3 {
  color: #0babea;
  font-size: 24px;
}
hr {
  background-color: #0babea;
  margin: 20px auto;
}
a {
  text-decoration: none;
  color: #0babea;
  font-size: 15px;
}
a:hover {
  color: coral;
}
.el-button {
  width: 45%;
  margin-left: 10px;
  background-color: #0babea;
}
.left-right-link {
  margin-left: 60px;
}
.inline-block {
  display: inline-block;
}
</style>
