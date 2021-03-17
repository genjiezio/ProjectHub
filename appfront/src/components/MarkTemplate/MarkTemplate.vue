<template>
  <div id="mark">
    <el-container class="all-background">
      <el-header style="text-align: left; font-size: 20px; color: #ffff">
        <el-row style="margin: auto 15%">
          <HeadLine v-bind:id="this.query"></HeadLine>
        </el-row>
      </el-header>

      <el-main>
        <div class="main-class">
          <br />
          <div style="margin: 0.5% 3%; width: 94%">
            <el-select v-model="cla" placeholder="请选择课程" style="width: 48%">
              <el-option v-for="item in classes" :key="item.$index" :label="item" :value="item">
              </el-option>
            </el-select>
            <el-select v-model="pro" placeholder="请选择Project" style="float: right; width: 48%" @change="update">
              <el-option v-for="(val, key) in pros[cla]" :key="key" :label="val.name" :value="val.id">
              </el-option>
            </el-select>
          </div>
          <div style="margin: 0.5% 3%; width: 96%">
            <el-button @click="isEdit = true" type="text"> 编辑 </el-button>
            <el-button @click="toAdd" type="text"> 添加 </el-button>
            <el-button @click="cancelSelect" type="text">取消选择</el-button>
            <el-button @click="editDone" type="text"> 完成 </el-button>
            <el-button @click="deleteDone" type="text"> 删除 </el-button>
            <uploadTemplate v-bind:tableData="tableData" v-bind:cla="cla" v-bind:pro="pro"></uploadTemplate>
          </div>
          <el-table ref="multipleTable" :data="tableData" tooltip-effect="dark" style="width: 96%; margin: auto 2%"
            @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55"> </el-table-column>
            <el-table-column prop="name" label="名称" width="120">
              <template slot-scope="scope">
                <div class="input-box" v-if="isEdit">
                  <el-input size="small" v-model="scope.row.name"></el-input>
                </div>
                <span v-else>{{ scope.row.name }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="fullScore" label="总分" width="100">
              <template slot-scope="scope">
                <div class="input-box" v-if="isEdit">
                  <el-input size="small" v-model="scope.row.fullScore"></el-input>
                </div>
                <span v-else>{{ scope.row.fullScore }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="desc" label="描述" width="300">
              <template slot-scope="scope">
                <div class="input-box" v-if="isEdit">
                  <el-input size="small" v-model="scope.row.desc"></el-input>
                </div>
                <span v-else>{{ scope.row.desc }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-main>
      <el-footer>
        <page-end></page-end>
      </el-footer>
    </el-container>
  </div>
</template>>

<script>
  import HeadLine from "../TeacherHeadLine";
  import pageEnd from "../pageEnd";
  import axios from "axios";
  import uploadTemplate from "./uploadTemplate";
  export default {
    components: {
      HeadLine,
      pageEnd,
      uploadTemplate
    },
    data() {
      return {
        tableData: [{
            name: "",
            fullScore: undefined,
            desc: "",
          }, 
        ],
        isEdit: false,
        multipleSelection: [],
        classes: [""],
        pros: {
          
        },
        query: "",
        cla: "",
        pro: "",
      };
    },
    created() {
      this.query = this.$route.query.qtid;
      axios
        .post("/teacher_api/get_class_pro", {
          tid: this.query,
        }, {
          headers: {
            "X-CSRFToken": document.cookie.split("=")[1],
          },
        })
        .then((res) => {
          this.tableData = [{
            name: "",
            fullScore: undefined,
            desc: "",
          }, ];
          this.classes = res.data.classes;
          this.pros = res.data.pros;
        });
      this.cla = "";
      this.pro = "";
    },
    methods: {
      cancelSelect() {
        this.$refs.multipleTable.clearSelection();
      },
      handleSelectionChange(rows) {
        rows.forEach((row) => {
          this.multipleSelection.push(row.name);
        });
      },
      deleteDone() {
        for (let i in this.tableData) {
          this.multipleSelection.forEach((row) => {
            if (row === this.tableData[i].name) {
              this.tableData.splice(i, 1);
            }
          });
        }
      },
      toAdd() {
        this.isEdit = true;
        this.tableData.push({
          id: undefined,
          name: "",
          fullScore: "",
          desc: "",
        });
      },
      update() {
        axios
          .post("/teacher_api/update_temp", {
            tid: this.query,
            class: this.cla,
            proid: this.pro,
          }, {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          })
          .then((res) => {
            if (res.data.status === 200) {
              this.tableData = res.data.tableData;
            } else {
              this.$message(res.data.msg);
            }
          });
      },
      editDone() {
        console.log(this.tableData);
        if (this.cla === "" || this.pro === "") {
          this.$message("请选择课程和Project");
          return;
        }
        this.isEdit = false;
        axios
          .post("/teacher_api/edit_temp", {
            tid: this.query,
            tableData: this.tableData,
            class: this.cla,
            proid: this.pro,
          }, {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          })
          .then((res) => {
            if (res.data.status === 200) {
              this.$message("成功修改");
            } else {
              this.$message(res.data.msg);
            }
          });
      },
    },
  };
</script>

<style scoped>
  .all-background {
    background-color: #f7f7f7;
    top: 0px;
    left: 0px;
    right: 0px;
    position: absolute;
    min-height: 110%;
  }

  .el-header {
    background-color: #ffffff;
    line-height: 60px;
  }

  .el-footer {
    background-color: #ffffff;
    line-height: 20px;
  }

  .main-class {
    width: 50%;
    margin-left: 25%;
    background-color: #ffffff;
  }

  .demo-table-expand {
    font-size: 0;
  }

  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }

  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
