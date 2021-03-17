<template>
  <el-upload
    class="upload-demo"
    :action="this.url + this.uploadUrl"
    :data="this.data"
    :on-success="onSuccess"
    style="display: inline-block; margin-left: 2%"
  >
    <el-button type="text">上传评分模板文件</el-button>
  </el-upload>
</template>

<script>
import axios from "axios";
export default {
  name: "uploadTemplate",
  props: ["tableData", "cla", "pro"],
  data() {
    return {
      childrenCla: "",
      childrenPro: 1,
      url: "",
      uploadUrl: "/teacher_api/upload_mark_file",
      data: {
        cla: this.childrenCla,
        proid: this.childrenPro,
        tid: this.$route.query.qtid,
      },
    };
  },
  created() {
    this.url = "http://127.0.0.1:8000";
  },
  watch: {
    pro(val) {
      if (val !== undefined) {
        this.childrenPro = val;
        this.data.proid = this.childrenPro;
        console.log(this.childrenPro);
      }
    },
  },

  methods: {
    onSuccess(response, file, fileList) {
      this.$message(response.status + ":" + response.msg);
      if (response.status === 200) {
        axios
          .post("/teacher_api/upload_mark_temp", {
            params: {
              tid: this.$route.query.qtid,
              cla: this.childrenCla,
              proid: this.childrenPro,
            },
          })
          .then((res) => {
            if (res.data.tableData) {
              for (let i = 0; i < res.data.tableData.length; i++) {
                this.$set(this.tableData, i, res.data.tableData[i]);
              }
            }
          });
      } else {
        this.$message("请选择课程和Project");
      }
    },
  },
};
</script>

<style scoped>
</style>
