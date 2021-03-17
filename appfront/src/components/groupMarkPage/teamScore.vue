<template>
  <div id="teamScore">
    <el-table
      :data="teamScore"
      border
      style="width: 100%">
      <el-table-column
        prop="id"
        label="序号"
        width="100">
      </el-table-column>
      <el-table-column
        prop="name"
        label="名称"
        width="120">
      </el-table-column>
      <el-table-column
        prop="getScore"
        label="评分"
        width="120">
      </el-table-column>
      <el-table-column
        prop="fullScore"
        label="总分"
        width="120">
      </el-table-column>
      <el-table-column
        prop="text"
        label="评价"
        width="380">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="120">
        <template slot-scope="scope">
          <el-row>
            <el-button type="text" @click="addShow(scope.row.id)" size="medium">编辑分数</el-button>
          </el-row>
          <el-row>
            <el-button type="text" @click="addShow1(scope.row.id)" size="medium">编辑评价</el-button>
          </el-row>

        </template>
      </el-table-column>
    </el-table>
    <!--弹窗数据-->
    <el-dialog title="更改分数"
               :visible.sync = dialogFormVisible
               :before-close="handleClose"
                style="text-align: center">
      <el-form>
        <el-form-item label="分数">
          <el-input
            oninput ="value=value.replace(/[^0-9.]/g,'')"
            v-model="point"
            placeholder="请输入各项分数"
          ></el-input>
        </el-form-item>
      </el-form>
      <el-button @click="dialogFormVisible = false">取 消</el-button>
      <el-button type="primary" @click="addDo">确 定</el-button>
    </el-dialog>
    <el-dialog title="更改评语"
               :visible.sync = dialogFormVisible1
               :before-close="handleClose">
      <el-form>
        <el-form-item  label="评语">
          <el-input
            v-model="text"
            placeholder="请给予评价"
          ></el-input>
        </el-form-item>
      </el-form>
      <el-button @click="dialogFormVisible1 = false">取 消</el-button>
      <el-button type="primary" @click="addTx">确 定</el-button>
    </el-dialog>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "teamScore",
  props:["teamScore"],
  data(){
    return{
      dialogFormVisible: false,
      dialogFormVisible1: false,
      index: 0,
      point: undefined,
      text: undefined,
      teamScoreChange:[]
    }
  },
  watch:{
    teamScore:{
      deep:true,
      handler:function (newValue,oldVal){
        console.log("just do it")
        console.log(this.teamScore)
        this.teamScoreChange=newValue
      }
    },
  },
  methods:{
    addShow(index) {
      this.index=index
      //显示弹窗
      this.dialogFormVisible = true;
    },
    addShow1(index) {
      this.index=index
      //显示弹窗
      this.dialogFormVisible1 = true;
    },
    handleClose(done) {

      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
    },
    addDo(){
      console.log("add")
      if(this.point<0){
        this.$message.error("最低分为0分");
      }
      else if(this.point>this.teamScore[this.index-1].fullScore){
        this.$message.error("超出最高分")
      }
      else {
        this.teamScore[this.index-1].getScore=parseFloat(this.point)
        this.dialogFormVisible = false;
        axios.post("/teacher_api/task_score",{
          key:this.teamScore[this.index-1].key,
          getScore:this.teamScore[this.index-1].getScore
        },{
          headers: {
            "X-CSRFToken": document.cookie.split("=")[1],
          }}).then((res)=>{})
        this.point=undefined
      }
    },
    addTx(){
      this.teamScore[this.index-1].text=this.text
      this.dialogFormVisible1 = false;
      axios.post("/teacher_api/task_comment",{
        key:this.teamScore[this.index-1].key,
        comment:this.teamScore[this.index-1].text
      },{
        headers: {
          "X-CSRFToken": document.cookie.split("=")[1],
        }}).then((res)=>{})
      this.text=undefined
    },
    fresh(){
      if(this.teamScore){
        if(this.teamScore.length===0){
          console.log("I got it")
        }
      }
    }
  }
}
</script>

<style scoped>
</style>
