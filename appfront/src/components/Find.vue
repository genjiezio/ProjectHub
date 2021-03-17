<template>
  <div id="app">
    <el-container class="all-background">
      <el-header style="text-align: left; font-size: 20px; color: #ffff">
        <el-row style="margin: auto 15%">
          <HeadLine v-bind:id="this.query"></HeadLine>
        </el-row>
      </el-header>

      <el-main>
        <div class="main-class">
          <div style="margin-bottom: 10px">
            <el-button :disabled="haveTeam" @click="addShow()">组队</el-button>
          </div>
          <el-table :data="tableData" style="width: 100%">
            <el-table-column type="expand">
              <template slot-scope="props">
                <el-form label-position="left">
                  <el-form-item label="技术栈:">
                    <br />
                    <template>
                      <li v-for="t in props.row.tech" :key="t.$index">
                        {{ t }}
                      </li>
                    </template>
                  </el-form-item>
                  <el-form-item label="组长:">
                    <el-link
                      :href="'/team/' + props.row.id + '?qsid='+ query"
                      :key="props.row.leader.id"
                      target="_self"
                      :underline="false"
                    >
                      {{ props.row.leader.name }}: {{ props.row.leader.job }}
                    </el-link>
                  </el-form-item>
                  <el-form-item label="描述:">
                    <br />
                    <span>{{ props.row.desc }}</span>
                  </el-form-item>
                  <el-form-item label="成员:">
                    <br />
                    <el-link
                      v-for="m in props.row.memb"
                      :href="'/' + m.id + '/information?qsid='+ query"
                      :key="m.name"
                      target="_self"
                      :underline="false"
                    >
                      {{ m.name }}: {{ m.job }}
                    </el-link>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column label="编号" prop="id" sortable> </el-table-column>
            <el-table-column label="组名" prop="name"> </el-table-column>
            <el-table-column label="Lab" prop="leader.lab"> </el-table-column>
            <el-table-column fixed="right" label="操作" width="100">
              <template slot-scope="scope">
                <el-button
                  @click="handleClick(scope.$index)"
                  :disabled="haveTeam"
                  type="text"
                  size="small"
                  >加入</el-button
                >
              </template>
            </el-table-column>
          </el-table>

          <!--弹窗数据-->
          <el-dialog
            title="组队"
            :visible.sync="dialogFormVisible"
            :before-close="handleClose"
          >
            <el-form :model="addObj" ref="addObj">
              <el-form-item label="分类">
                <el-select
                  v-model="addObj.category"
                  placeholder="请选择"
                  style="width: 100%"
                >
                  <el-option
                    v-for="item in proCate"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="您将用到哪些技术">
                <el-input
                  v-model="addObj.tech"
                  auto-complete="off"
                  placeholder="请用,分隔"
                ></el-input>
              </el-form-item>
              <el-form-item label="描述">
                <el-input
                  type="textarea"
                  :rows="2"
                  placeholder="请描述您希望做一个怎么样的Project"
                  v-model="addObj.desc"
                >
                </el-input>
              </el-form-item>
              <el-form-item label="希望参与哪一部分的工作">
                <el-input
                  v-model="addObj.membJob"
                  auto-complete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="是否希望系统分配队友">
                <el-radio-group v-model="addObj.isAccept">
                  <el-radio :label="true">是</el-radio>
                  <el-radio :label="false">否</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="是否新建一个组" v-if="addObj.isAccept">
                <el-radio v-model="addObj.isNew" :label="true">是</el-radio>
                <el-radio v-model="addObj.isNew" :label="false">否</el-radio>
              </el-form-item>
              <el-form-item
                label="请您为您的小组取一个有趣的名字"
                v-if="addObj.isNew"
              >
                <el-input v-model="addObj.name" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item
                label="您希望队友熟悉的知识(用,分隔)"
                v-if="addObj.isNew && addObj.isAccept"
              >
                <el-input
                  v-model="addObj.desiTech"
                  auto-complete="off"
                ></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="addDo">确 定</el-button>
            </div>
          </el-dialog>

          <!--弹窗数据-->
          <el-dialog
            title="加入小组"
            :visible.sync="addDialogFormVisible"
            :before-close="handleClose"
          >
            <el-form>
              <el-form-item label="希望参与哪一部分的工作">
                <el-select
                  v-model="info.job"
                  placeholder="请选择"
                  style="width: 100%"
                >
                  <el-option
                    v-for="item in proCate"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="您熟悉的技术">
                <el-input
                  v-model="info.tech"
                  auto-complete="off"
                  placeholder="请用,分隔"
                ></el-input>
              </el-form-item>
              <el-form-item label="加入理由">
                <el-input
                  type="textarea"
                  :rows="2"
                  placeholder="请输入内容"
                  v-model="info.desc"
                >
                </el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="addDialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="join">确 定</el-button>
            </div>
          </el-dialog>
        </div>
      </el-main>
      <el-footer>
        <page-end></page-end>
      </el-footer>
    </el-container>
  </div>
</template>>

<script>
import HeadLine from "./HeadLine";
import pageEnd from "./pageEnd";
import axios from "axios";
export default {
  components: { HeadLine, pageEnd },
  data() {
    return {
      tableData: [
        {
          id: "",
          name: "",
          desc: "",
          tech: [""],
          memb: [{ id: "", name: "", job: "" }],
          leader: { id: "", name: "", job: "", lab: undefined },
        },

      ],
      dialogFormVisible: false,
      addDialogFormVisible: false,
      haveTeam: false,
      addObj: {
        name: "",
        category: "",
        desc: "",
        tech: "",
        isAccept: false,
        isNew: true,
        desiTech: "",
      },
      info: {
        tech: "",
        job: "",
        desc: "",
      },
      proCate: [
        {
          value: "",
          label: "",
        },
      ],
      teamIndex: 1,
      query: "1",
      intervalId: null,
    };
  },
  created() {
    this.query = this.$route.query.qsid;
    axios
      .post("/student_api/get_team", {
        sid: this.query,
        pid: this.$route.params.pid,
      }, {
        headers: {
          "X-CSRFToken": document.cookie.split("=")[1],
        },
      })
      .then((res) => {
        this.tableData = res.data.tableData;
        this.proCate = res.data.proCate;
        this.haveTeam = res.data.haveTeam;
      });
      this.dataRefresh();
  },
  methods: {
    dataRefresh() {
      // 计时器正在进行中，退出函数
      if (this.intervalId != null) {
        return;
      }
      // 计时器为空，操作
      this.intervalId = setInterval(() => {
        console.log("刷新" + new Date());
        axios
          .post("/student_api/get_team", {
            sid: this.query,
            pid: this.$route.params.pid,
          }, {
        headers: {
          "X-CSRFToken": document.cookie.split("=")[1],
        },
      })
          .then((res) => {
            this.tableData = res.data.tableData;
            this.proCate = res.data.proCate;
            this.haveTeam = res.data.haveTeam;
          });
      }, 5000);
    },
    // 停止定时器
    clear() {
      clearInterval(this.intervalId); //清除计时器
      this.intervalId = null; //设置为null
    },
    addShow() {
      //显示弹窗
      this.dialogFormVisible = true;
    },
    addDo() {
      this.dialogFormVisible = false;
      axios
        .post(
          "/student_api/create_team",
          {
            addTeam: {
              name: this.addObj.name,
              desc: this.addObj.desc,
              tech: this.addObj.tech,
              category: this.addObj.category,
              isAccept: this.addObj.isAccept,
              isNew: this.addObj.isNew,
              desiTech: this.addObj.desiTech,
            },
            sid: this.query,
            pid: this.$route.params.pid,
          },
          {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          }
        )
        .then((res) => {
          if (res.data.status == 200) {
            this.tableData = res.data.tableData;
            alert("成功创建");
          } else {
            alert(res.data.msg);
          }
        });
    },
    handleClick(index) {
      this.addDialogFormVisible = true;
      this.teamIndex = index;
    },
    join() {
      this.addDialogFormVisible = false;
      axios
        .post(
          "/student_api/join_team",
          {
            gid: this.tableData[this.teamIndex].id,
            info: this.info,
            sid: this.query,
            pid: this.$route.params.pid,
          },
          {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          }
        )
        .then((res) => {
          if (res.data.status == 200) {
            alert("成功发送加入请求");
          } else {
            alert(res.data.msg);
          }
        });
    },
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {});
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
