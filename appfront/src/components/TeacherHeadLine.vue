<template>
  <div class="TeacherHeadLine">
    <el-row>
      <el-col :span="6" class="Title">
        <el-image
          style="width: 127px; height: 46px; margin-top: 7px"
          :src="logo_url"
        ></el-image>
      </el-col>
      <el-col :span="2" :offset="5">
        <el-link :href="'/teacher/' + id" target="_self" :underline="false"
        >主页</el-link
        >
      </el-col>
      <el-col :span="2" :offset="9" style="line-height: 10px">
        <br />
        <el-popover placement="bottom" width="300" trigger="hover">
          <el-row style="height: 15px">
            <el-col :span="6" class="inf">
              <br />
              FFFancy
            </el-col>
          </el-row>
          <el-divider></el-divider>
          <el-row style="text-align: center">
            <el-col :span="12">
              <el-link
                :href="'/teacher/' + id + '?aname=1'"
                target="_self"
                :underline="false"
              >
                <el-row>
                  <i class="el-icon-date" style="font-size: 36px"></i>
                </el-row>
                <el-row> 日历 </el-row>
              </el-link>
            </el-col>
            <el-col :span="12">
              <el-link
                :href="'/teacher/' + id + '?aname=2'"
                target="_self"
                :underline="false"
              >
                <el-row>
                  <i class="el-icon-monitor" style="font-size: 36px"></i>
                </el-row>
                <el-row> 小组管理 </el-row>
              </el-link>
            </el-col>
          </el-row>
          <br>
          <el-row style="text-align: center">
            <el-col :span="12">
              <el-link
                :href="'/teacher/' + id + '?aname=3'"
                target="_self"
                :underline="false"
              >
                <el-row>
                  <i class="el-icon-view" style="font-size: 36px"></i>
                </el-row>
                <el-row> 学生管理 </el-row>
              </el-link>
            </el-col>
            <el-col :span="12">
              <el-link
                :href="'/teacher/' + id + '?aname=4'"
                target="_self"
                :underline="false"
              >
                <el-row>
                  <i class="el-icon-folder" style="font-size: 36px"></i>
                </el-row>
                <el-row> 项目管理 </el-row>
              </el-link>
            </el-col>
          </el-row>

          <el-divider style="line-height: 1px"></el-divider>
          <el-row style="text-align: center; margin-bottom: 2px">
            <el-col :span="12">
              <el-link
                href="/findpassword"
                target="_self"
                :underline="false"
              >
                <i class="el-icon-setting" style="font-size: 15px"> 账号设置</i>
              </el-link>
            </el-col>
            <el-col :span="12">
              <el-link href="/login" target="_self" :underline="false"  @click="loginOut">
                <a
                  class="el-icon-turn-off"
                  style="font-size: 15px; float: center"
                >
                  退出登录</a
                >
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
export default {
  name: "TeacherHeadLine",
  props: ["id"],
  data() {
    return {
      logo_url: "/static/logo1.png",
      fig:
        "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
    };
  },
  methods:{
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
  }
}
</script>

<style scoped>

</style>
