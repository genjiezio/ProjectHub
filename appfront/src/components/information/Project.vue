<template>
  <div id="project">
    <div class="content">
      <el-row>
        <span style="display: inline-block; font-size: 28px"> 参与项目 </span>
      </el-row>
      <el-divider></el-divider>
      <li
        v-for="key in infoProject"
        :key="key.name"
        style="list-style-type: none; margin-bottom: 2%"
      >
        <el-card class="box-card">
          <div slot="header">
            <span>{{ key.name }}</span>
            <el-button
              style="float: right; padding: 5px 1px"
              type="text"
              icon="el-icon-close"
              @click="deleteProject(key)"
            ></el-button>
          </div>
          <div v-for="(k, v) in key" :key="k">
            <el-col :span="2" class="value-text">{{ v }}:</el-col>
            <el-col :span="21" class="key-text">{{ k }}</el-col>
          </div>
          <el-row></el-row>
        </el-card>
      </li>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Basic",
  props: ["query"],
  data() {
    return {
      infoProject: [
        {
          name: "",
          date: "",
          url: "",
          desc: "",
        },
      ],
    };
  },
  created() {
    axios
      .post(
        "/student_api/get_info_project",
        { sid: this.$route.params.sid },
        {
          headers: {
            "X-CSRFToken": document.cookie.split("=")[1],
          },
        }
      )
      .then((res) => {
        this.infoProject = res.data.project;
      });
  },
  methods: {
    deleteProject(key) {
      if (this.query !== undefined) {
        this.$message("你为什么想改别人的信息？");
        return;
      }
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
</style>
