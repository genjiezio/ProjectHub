<template>
  <div id="app">
    <el-container class="all-background">
      <el-header>
        <el-row class="demo-avatar demo-basic">
          <div class="basic--circle">
            <div class="avatar">
              <el-button
                type="plain"
                icon="el-icon-user"
                circle
                @click="goToInformation"
              ></el-button>
            </div>
          </div>
        </el-row>
      </el-header>

      <el-main>
        <div class="main-class">
          <el-divider content-position="center">正在进行的Project</el-divider>
          <div style="margin-bottom: 10px">
            <el-button @click="addShow()">新建Project</el-button>
          </div>
          <el-table :data="tableData" style="width: 100%">
            <el-table-column type="expand">
              <template slot-scope="props">
                <el-form label-position="left">
                  <el-form-item label="技术栈：">
                    <br />
                    <template>
                      <li v-for="t in props.row.tech" :key="t.name">
                        {{ t.name }}
                      </li>
                    </template>
                  </el-form-item>
                  <el-form-item label="描述：">
                    <br />
                    <span>{{ props.row.desc }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column label="编号" prop="id" sortable> </el-table-column>
            <el-table-column label="Project名" prop="name"> </el-table-column>
            <el-table-column label="开始时间" prop="startTime" sortable>
            </el-table-column>
            <el-table-column label="截止时间" prop="endTime" sortable>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  @click="handleEdit(scope.$index, scope.row)"
                  >编辑</el-button
                >
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>
          <br/>
          <el-divider content-position="center">已截止Project</el-divider>
          <el-table :data="tableData" style="width: 100%">
            <el-table-column type="expand">
              <template slot-scope="props">
                <el-form label-position="left">
                  <el-form-item label="技术栈：">
                    <br />
                    <template>
                      <li v-for="t in props.row.tech" :key="t.name">
                        {{ t.name }}
                      </li>
                    </template>
                  </el-form-item>
                  <el-form-item label="描述：">
                    <br />
                    <span>{{ props.row.desc }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column label="编号" prop="id" sortable> </el-table-column>
            <el-table-column label="Project名" prop="name"> </el-table-column>
            <el-table-column label="开始时间" prop="startTime" sortable>
            </el-table-column>
            <el-table-column label="截止时间" prop="endTime" sortable>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>

          <!--弹窗数据-->
          <el-dialog title="新建Project" :visible.sync="dialogFormVisible"
            :before-close="handleClose">
            <el-form>
              <el-form-item label="Project名">
                <el-input v-model="addObj.name" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item label="开始时间">
                <el-input
                  v-model="addObj.startTime"
                  auto-complete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="截止时间">
                <el-input
                  v-model="addObj.endTime"
                  auto-complete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="描述">
                <el-input
                  type="textarea"
                  :rows="2"
                  placeholder="请输入内容"
                  v-model="addObj.desc"
                >
                </el-input>
              </el-form-item>
              <el-form-item label="技术栈">
                <el-input
                  v-model="addObj.tech"
                  auto-complete="off"
                  placeholder="请用,分隔"
                ></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="addDo">确 定</el-button>
            </div>
          </el-dialog>
          <!--弹窗数据-->
          <el-dialog title="编辑Project信息" :visible.sync="addDialogFormVisible"
            :before-close="handleClose">
            <el-form>
              <el-form-item label="Project名">
                <el-input v-model="addObj.name" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item label="开始时间">
                <el-input
                  v-model="addObj.startTime"
                  auto-complete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="截止时间">
                <el-input
                  v-model="addObj.endTime"
                  auto-complete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="描述">
                <el-input
                  type="textarea"
                  :rows="2"
                  placeholder="请输入内容"
                  v-model="addObj.desc"
                >
                </el-input>
              </el-form-item>
              <el-form-item label="tech">
                <el-input
                  v-model="addObj.tech"
                  auto-complete="off"
                  placeholder="请用,分隔"
                ></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="addDialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="addDo">确 定</el-button>
            </div>
          </el-dialog>
        </div>
      </el-main>
    </el-container>
  </div>
</template>>

<script>
import axios from "axios";
export default {
  data() {
    return {
      tableData: [
        {
          id: "1",
          name: "鸡蛋仔",
          startTime: Date("2020-10-1"),
          endTime: Date("2020-10-8"),
          desc: "荷兰优质淡奶，奶香浓而不腻",
          tech: ["Python" , "Vue" ],
        },
        {
          id: "1",
          name: "鸡蛋仔",
          startTime: Date("2020-10-1"),
          endTime: Date("2020-10-8"),
          desc: "荷兰优质淡奶，奶香浓而不腻",
          tech: ["Python" , "Vue"],
        },
        {
          id: "1",
          name: "鸡蛋仔",
          startTime: Date("2020-10-1"),
          endTime: Date("2020-10-8"),
          desc: "荷兰优质淡奶，奶香浓而不腻",
          tech: ["Python", "Vue" ],
        },
      ],
      //头像url
      avatar_url:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      dialogFormVisible: false,
      addDialogFormVisible: false,
      addObj: {
        id: "",
        name: "",
        startTime: Date(""),
        endTime: Date(""),
        desc: "",
        tech: "",
      },
      editIndex: 1,
    };
  },
  created() {
    axios.get("/tpage/", {}).then((res) => {
      this.tableData = res.data.tableData
      this.avatar_url = res.data.avatar_url
    });
  },
  methods: {
    handleClick(length) {
      console.log(length);
    },
    goToInformation() {
      window.location.href = "http://localhost:8086/information";
    },
    handleEdit(index, row) {
      //显示弹窗
      this.addDialogFormVisible = true;
      this.addObj = this.tableData[index];
      this.addObj.tech = this.addObj.tech.toString();
      console.log(this.addObj);
      this.editIndex = index;
    },
    confirmEdit(){
      axios.post("/tpage/", {index: this.editindex, addObj: this.addObj},
          {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          })
           .then((res) => {
             if (res.data.status == 200){
               alert("修改成功")
             }else if(res.data.status == 401){
               alert("Project已存在")
             }else{
               alert("非法输入")
             }
             this.tableData = res.data.tableData
           });
    },
    handleDelete(index, row) {
      axios.post("/tpage/", {index: index, row: row},
          {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          })
           .then((res) => {
             if (res.status == 200){
               alert("成功删除")
             }
             this.tableData = res.tableData
           });
    },
    addShow() {
      //记录id
      this.addObj.id = this.tableData.length + 1;
      //显示弹窗
      this.dialogFormVisible = true;
    },
    addDo() {
      this.dialogFormVisible = false;
      axios.post("/tpage/", {addObj: this.addObj},
          {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          })
           .then((res) => {
             if (res.data.status == 200){
               alert("成功创建")
             }else if(res.data.status == 401){
               alert("Project已存在")
             }else{
               alert("非法输入")
             }
             this.tableData = res.tableData
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
  min-height: 100%;
}

.el-header {
  background-color:rgb(24, 26, 27);
  line-height: 60px;
}

.main-class {
  width: 70%;
  margin-left: 15%;
}

.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
.avatar {
  margin-top: 0.05%;
  display: block;
  float: right;
}
</style>