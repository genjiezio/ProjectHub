<template>
  <div class="login clearfix">
    <div class="login-wrap">
      <el-row type="flex" justify="center">
        <el-form
          :rules="rules"
          ref="user"
          :model="user"
          status-icon
          label-width="80px"
        >
          <h3>注册</h3>
          <hr />
          <el-form-item prop="username" label="用户名">
            <el-input
              v-model="user.username"
              placeholder="请输入用户名"
            ></el-input>
          </el-form-item>
          <el-form-item prop="email" label="邮箱">
            <el-input v-model="user.email" placeholder="请输入邮箱"></el-input>
            <el-button type="text" :disabled="disabled" @click="sendMail">{{
              btntxt
            }}</el-button>
          </el-form-item>
          <el-form-item prop="checkid" label="验证码">
            <el-input
              v-model="user.checkid"
              placeholder="请输入验证码"
            ></el-input>
          </el-form-item>
          <el-form-item prop="password" label="设置密码">
            <el-input
              v-model="user.password"
              show-password
              placeholder="请输入密码"
            ></el-input>
          </el-form-item>
          <el-form-item prop="repassword" label="确认密码">
            <el-input
              v-model="user.repassword"
              show-password
              placeholder="确认密码"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              class="main-button"
              type="primary"
              @click="submitForm('user')"
              >提交</el-button
            >
            <el-button class="main-button" @click="resetForm('user')"
              >重置</el-button
            >
          </el-form-item>
        </el-form>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "register",
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.user.repassword !== "") {
          this.$refs.user.validateField("repassword");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.user.password) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      disabled: false,
      time: 0,
      btntxt: "获取验证码",
      user: {
        username: "",
        email: "",
        password: "",
        checkid: "",
        repassword: "",
      },
      rules: {
        password: [{ validator: validatePass, trigger: "blur" }],
        repassword: [{ validator: validatePass2, trigger: "blur" }],
      },
    };
  },
  created() {
    axios.get("/padmin_api/get_csrf_token", {}).then((res) => {
      this.csrf_token = res.data.csrf_token;
    });
  },
  methods: {
    timer() {
      if (this.time > 0) {
        this.time--;
        this.btntxt = this.time + "s后重新获取";
        setTimeout(this.timer, 1000);
      } else {
        this.time = 0;
        this.btntxt = "获取验证码";
        this.disabled = false;
      }
    },
    sendMail() {
      if (!this.user.username) {
        this.$message.error("请输入用户名！");
        return;
      } else if (!this.user.email) {
        this.$message.error("请输入邮箱！");
        return;
      } else if (this.user.email != null) {
        var reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
        if (!reg.test(this.user.email)) {
          this.$message.error("请输入有效的邮箱！");
        } else {
          this.time = 60;
          this.disabled = true;
          this.timer();
          axios
            .post(
              "/student_api/verify",
              {
                email: this.user.email,
              },
              {
                headers: {
                  "X-CSRFToken": this.csrf_token,
                },
              }
            )
            .then((res) => {
              if (res.data.status != 200) {
                this.$message(res.data.msg);
              } else {
                this.$message("验证码已发送至您的邮箱");
              }
            });
        }
      }
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios
            .post(
              "/student_api/find_account",
              {
                name: this.user.username,
                email: this.user.email,
                password: this.user.password,
                code: this.user.checkid,
              },
              {
                headers: {
                  "X-CSRFToken": this.csrf_token,
                },
              }
            )
            .then((res) => {
              if (res.data.status === 200) {
                this.$message("成功注册");
                this.$router.push({ path: "/login" });
              } else if (res.data.status === 400) {
                this.$message("验证码错误");
              } else {
                this.$message("状态异常，请稍候操作");
              }
            });
          return true;
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
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
  width: 450px;
  height: 520px;
  margin: 6% auto;
  padding-top: 10px;
  border-radius: 5px;
  background: #ffffff;
}
h3 {
  color: #0babea;
  font-size: 24px;
}
hr {
  background-color: #0babea;
  margin: 20px auto;
}

.main-button {
  width: 30%;
}
</style>
