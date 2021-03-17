<template>
  <div id="skill">
    <div class="content">
      <el-row>
        <span style="display: inline-block; font-size: 28px"> 掌握技能 </span>
        <span>
          <el-button v-if="toEditSkill" id="edit-button" @click="skillButton">编辑</el-button>
          <el-button v-else id="edit-button" @click="skillEditDone">完成</el-button>
        </span>
      </el-row>
      <el-divider></el-divider>
      <el-tag v-for="(v, k) in infoSkill" :key="k" :closable="!toEditSkill" style="margin-right: 1%" @close="handleSkillDelete(k)">
        <span>{{ k }}</span>
      </el-tag>
      <el-input class="input-new-tag" v-if="inputVisible" v-model="inputValue" ref="saveTagInput" size="small"
        placeholder="技能: 熟练度" @keyup.enter.native="handleInputConfirm" @blur="handleInputConfirm">
      </el-input>
      <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 添加/更新技能</el-button>
      <li v-for="(v, k, index) in infoSkill" :key="index" style="list-style-type: none; margin: 4% auto">
        <el-row>
          <el-col :span="3" class="value-text"> {{ k }} </el-col>
          <el-col :span="18" :push="1">
            <el-progress :text-inside="true" :stroke-width="22" :percentage="v"></el-progress>
          </el-col>
        </el-row>
      </li>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  export default {
    name: "Skill",
    props: ["query"],
    data() {
      return {
        toEditSkill: true,
        inputVisible: false,
        inputValue: "",
        infoSkill: {
          github: undefined
        }
      };
    },
    created() {
      axios.post("/student_api/get_info_skill", {
        sid: this.$route.params.sid
      }, {
        headers: {
          "X-CSRFToken": document.cookie.split("=")[1],
        },
      }).then((res) => {
        this.infoSkill = res.data.skill;
      });
    },
    methods: {
      skillButton() {
        if (this.query !== undefined) {
          this.$message("你为什么想改别人的信息？");
          return;
        }
        this.toEditSkill = false;
      },
      handleSkillDelete(k) {
        axios
          .post(
            "/student_api/delete_info_skill", {
              sid: this.$route.params.sid,
              skill: k
            }, {
              headers: {
                "X-CSRFToken": document.cookie.split("=")[1],
              },
            }
          )
          .then((res) => {
            this.infoSkill = res.data.skill;
          });
      },
      showInput() {
        this.inputVisible = true;
        this.$nextTick((_) => {
          this.$refs.saveTagInput.$refs.input.focus();
        });
      },
      skillEditDone() {
        this.toEditSkill = true;
      },
      handleInputConfirm() {
        if (this.query !== undefined) {
          this.toEditUser = false;
          this.$message("你为什么想改别人的信息？");
          return;
        }
        let inputValue = this.inputValue;
        if (inputValue) {
          axios
            .post(
              "/student_api/add_info_skill", {
                sid: this.$route.params.sid,
                str: inputValue
              }, {
                headers: {
                  "X-CSRFToken": document.cookie.split("=")[1],
                },
              }
            )
            .then((res) => {
              this.infoSkill = res.data.skill;
            });
        }
        this.inputVisible = false;
        this.inputValue = "";
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

  .value-text {
    font-size: 16px;
    text-align: right;
    color: #303133;
  }
</style>
