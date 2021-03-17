<template>
  <div id="app">
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
                <el-avatar :src="user.avator" :size="65"></el-avatar>
              </el-col>
              <el-col :span="16">
                <el-row style="height: 15px">{{ user.id }}</el-row>
                <el-row>
                  <ul style="float: left; padding: 0 0">
                    <li class="el-icon-s-check">
                      <a> {{ user.edu }} </a>
                    </li>
                    &nbsp;
                    <li class="el-icon-school">
                      <a> {{ user.school }} </a>
                    </li>
                    &nbsp;
                    <li class="el-icon-cpu">
                      <a> {{ user.major }} </a>
                    </li>
                  </ul>
                </el-row>
              </el-col>
              <el-col style="margin-top: 1.5%" :span="3">
                <el-button @click="toEditUser = true">编辑</el-button>
              </el-col>
              <el-dialog title="修改信息" :visible.sync="toEditUser">
                <el-form :model="user">
                  <el-form-item label="昵称" label-width="120px">
                    <el-input v-model="user.id" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="学历" label-width="120px">
                    <el-select v-model="user.edu" placeholder="请选择学历">
                      <el-option label="本科" value="本科"></el-option>
                      <el-option label="硕士" value="硕士"></el-option>
                      <el-option label="博士" value="博士"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="学校" label-width="120px">
                    <el-input
                      v-model="user.school"
                      autocomplete="off"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="专业" label-width="120px">
                    <el-input
                      v-model="user.major"
                      autocomplete="off"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="头像" label-width="120px">
                    <el-upload
                      class="avatar-uploader"
                      action="https://jsonplaceholder.typicode.com/posts/"
                      :show-file-list="false"
                      :on-success="handleAvatarSuccess"
                      :before-upload="beforeAvatarUpload"
                    >
                      <img
                        v-if="user.avator"
                        :src="user.avator"
                        class="avatar"
                      />
                      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                    </el-upload>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="toEditUser = false">取 消</el-button>
                  <el-button type="primary" @click="editUserDo"
                    >确 定</el-button
                  >
                </div>
              </el-dialog>
            </el-row>
          </el-card>
          <el-card class="mid-card">
            <el-tabs tab-position="left">
              <el-tab-pane>
                <span slot="label"><i class="el-icon-user"></i>基本资料</span>
                <div class="content">
                  <el-row>
                    <span style="display: inline-block; font-size: 28px"
                      >基本资料</span
                    >
                    <span>
                      <el-button
                        v-if="toEditBasic"
                        id="edit-button"
                        @click="BasicButton"
                        >编辑</el-button
                      >
                      <el-button v-else id="edit-button" @click="BasicEditDone"
                        >完成</el-button
                      >
                    </span>
                  </el-row>
                  <el-divider></el-divider>
                  <el-form ref="addBasic" :model="addBasic" label-width="20%">
                    <el-form-item label="我的姓名">
                      <span v-if="toEditBasic">{{ info.basic.name }}</span>
                      <span v-else>
                        <el-input
                          v-model="addBasic.name"
                          minlength="1"
                        ></el-input>
                      </span>
                    </el-form-item>
                    <el-form-item label="我的性别">
                      <span v-if="toEditBasic">{{ info.basic.sex }}</span>
                      <span v-else>
                        <el-radio v-model="addBasic.sex" label="男"
                          >男</el-radio
                        >
                        <el-radio v-model="addBasic.sex" label="女"
                          >女</el-radio
                        >
                      </span>
                    </el-form-item>
                    <el-form-item label="我的简介">
                      <span v-if="toEditBasic">{{ info.basic.desc }}</span>
                      <span v-else>
                        <el-input type="textarea" :rows="2" v-model="textarea">
                        </el-input>
                      </span>
                    </el-form-item>
                    <el-form-item label="居住地">
                      <span v-if="toEditBasic">{{ info.basic.area }}</span>
                      <span v-else>
                        <el-input v-model="addBasic.area"></el-input>
                      </span>
                    </el-form-item>
                    <el-form-item label="我的专业">
                      <span v-if="toEditBasic">{{ info.basic.major }}</span>
                      <span v-else>
                        <el-input v-model="addBasic.major"></el-input>
                      </span>
                    </el-form-item>
                    <el-form-item label="毕业年份">
                      <span v-if="toEditBasic">{{ info.basic.gyear }}</span>
                      <span v-else>
                        <el-date-picker v-model="addBasic.gyear" type="year">
                        </el-date-picker>
                      </span>
                    </el-form-item>
                    <el-form-item label="毕业意向">
                      <span v-if="toEditBasic">{{ info.basic.willing }}</span>
                      <span v-else>
                        <el-input v-model="addBasic.willing"></el-input>
                      </span>
                    </el-form-item>
                  </el-form>
                </div>
              </el-tab-pane>
              <el-tab-pane>
                <span slot="label"
                  ><i class="el-icon-collection"></i>掌握技能</span
                >
                <div class="content">
                  <el-row>
                    <span style="display: inline-block; font-size: 28px">
                      掌握技能
                    </span>
                    <span>
                      <el-button
                        v-if="toEditSkill"
                        id="edit-button"
                        @click="skillButton"
                        >编辑</el-button
                      >
                      <el-button v-else id="edit-button" @click="skillEditDone"
                        >完成</el-button
                      >
                    </span>
                  </el-row>
                  <el-divider></el-divider>
                  <el-tag
                    v-for="(v, k) in info.skill"
                    :key="k"
                    :closable="skillEdit"
                    style="margin-right: 1%"
                    @close="handleSkillDelete(k)"
                  >
                    <span>{{ k }}</span>
                  </el-tag>
                  <el-input
                    class="input-new-tag"
                    v-if="inputVisible"
                    v-model="inputValue"
                    ref="saveTagInput"
                    size="small"
                    placeholder="技能: 熟练度"
                    @keyup.enter.native="handleInputConfirm"
                    @blur="handleInputConfirm"
                  >
                  </el-input>
                  <el-button
                    v-else
                    class="button-new-tag"
                    size="small"
                    @click="showInput"
                    >+ 添加/更新技能</el-button
                  >
                  <li
                    v-for="(v, k) in info.skill"
                    :key="k"
                    style="list-style-type: none; margin: 4% auto"
                  >
                    <el-row>
                      <el-col :span="3" class="value-text"> {{ k }} </el-col>
                      <el-col :span="18" push="1"
                        ><el-progress
                          :text-inside="true"
                          :stroke-width="22"
                          :percentage="v"
                        ></el-progress
                      ></el-col>
                    </el-row>
                  </li>
                </div>
              </el-tab-pane>
              <el-tab-pane>
                <span slot="label"><i class="el-icon-folder"></i>参与项目</span>
                <div class="content">
                  <el-row>
                    <span style="display: inline-block; font-size: 28px">
                      参与项目
                    </span>
                  </el-row>
                  <el-divider></el-divider>
                  <li
                    v-for="key in info.project"
                    :key="key.name"
                    style="list-style-type: none; margin-bottom: 2%"
                  >
                    <el-card class="box-card">
                      <div slot="header">
                        <a :href="key.url">{{ key.name }}</a>
                        <el-button
                          style="float: right; padding: 5px 1px"
                          type="text"
                          @click="deleteProject(key)"
                          >删除</el-button
                        >
                      </div>
                      <div v-for="(k, v) in key" :key="k">
                        <el-col :span="3" class="value-text">{{ v }}:</el-col>
                        <el-col :span="18" class="key-text">{{ k }}</el-col>
                      </div>
                      <el-row></el-row>
                    </el-card>
                  </li>
                </div>
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
</template>>

<script>
import axios from "axios";
import HeadLine from "./HeadLine";
import pageEnd from "./pageEnd";
export default {
  name: "app",
  components: { pageEnd, HeadLine },
  data() {
    return {
      info: {
        basic: {
          name: "Tim",
          sex: "男",
          desc: "垃圾",
          area: "深圳",
          major: "CS",
          gyear: 2022,
          willing: "咸鱼",
        },
        skill: { github: 50, python: 30, java: 20, "C++": 40, vue: 100 },
        project: [
          {
            name: "Python",
            date: "2020-10-22",
            url: "www.github.com",
            desc: "terrible",
          },
        ],
      },
      user: {
        id: "Lloyd",
        avator:
          "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
        edu: "本科",
        school: "南方科技大学",
        major: "计算机科学与工程系",
      },
      skillEdit: false,
      inputVisible: false,
      inputValue: "",
      toEditSkill: true,
      toEditBasic: true,
      toEditUser: false,
      addBasic: {
        name: "",
        sex: "",
        desc: "",
        area: "",
        major: "",
        gyear: 2020,
        willing: "",
      },
    };
  },
  inject: ["reload"],
  created() {
    axios.get("student_api/get_information", {}).then((res) => {
      this.info.basic = res.data.basic;
      this.info.skill = res.data.skill;
      this.info.project = res.data.project;
      this.user = res.data.user;
      this.reload();
    });
  },
  methods: {
    handleAvatarSuccess(res, file) {
      this.user.avator = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error("上传头像图片只能是 JPG 格式!");
      }
      if (!isLt2M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
      }
      return isJPG && isLt2M;
    },
    editUserDo() {
      axios.post("student_api/edit_user", {user: user}).then((res) => {
        if (res.data.status == 200){
          this.user = res.data.user;
        }
        alert(res.data.msg);
      });
      this.toEditUser = false;
    },
    goBack() {
      window.history.back();
      console.log("go back");
    },
    skillButton() {
      this.skillEdit = true;
      this.toEditSkill = false;
    },
    BasicButton() {
      this.toEditBasic = false;
    },
    BasicEditDone() {
      this.toEditBasic = true;
      axios
        .post(
          "student_api/edit_info_basic",
          { basic: addBasic },
          {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          }
        )
        .then((res) => {
          this.info.basic = res.data.basic;
          this.reload();
        });
    },
    handleSkillDelete(k) {
      axios
        .post(
          "student_api/delete_info_skill",
          { skill: k },
          {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          }
        )
        .then((res) => {
          this.info.skill = res.data.skill;
          this.reload();
        });
    },
    deleteProject(key) {
      axios
        .post(
          "student_api/delete_info_project",
          { project: key },
          {
            headers: {
              "X-CSRFToken": document.cookie.split("=")[1],
            },
          }
        )
        .then((res) => {
          this.info.project = res.data.project;
          this.reload();
        });
    },
    showInput() {
      this.inputVisible = true;
      this.$nextTick((_) => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    skillEditDone() {
      this.skillEdit = false;
      this.toEditSkill = true;
    },
    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        axios
          .post(
            "student_api/add_info_skill",
            { str: inputValue },
            {
              headers: {
                "X-CSRFToken": document.cookie.split("=")[1],
              },
            }
          )
          .then((res) => {
            this.info.skill = res.data.skill;
            this.reload();
          });
      }
      this.inputVisible = false;
      this.inputValue = "";
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
  margin-left: 10%;
  font-size: 25px;
  color: #ffffff;
}

.value-text {
  margin-left: 5%;
  font-size: 20px;
  text-align: center;
  color: rgb(168, 160, 149);
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
