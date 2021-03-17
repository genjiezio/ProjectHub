<template>
  <div id="personalScore">
    <el-card class="box-card">
      <el-table
        :data="personalScore"
        border
        style="width: 100%">
        <el-table-column
          prop="id"
          label="序号"
          width="80">
        </el-table-column>
        <el-table-column
          prop="name"
          label="姓名"
          width="80">
        </el-table-column>
        <el-table-column
          prop="score"
          label="评分"
          width="100">
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          width="120">
          <template slot-scope="scope">
            <el-row>
              <el-button type="text" @click="addShow(scope.row.id)" size="medium">编辑分数</el-button>
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
              v-model="point"
              placeholder="请输入学生分数"
            ></el-input>
          </el-form-item>
        </el-form>
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="addDo">确 定</el-button>
      </el-dialog>
    </el-card>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "personalScore",
  props:["personalScore"],
  data(){
    return{
      dialogFormVisible: false,
      index: 0,
      point: undefined,
      text:"text",
      pastScore:NaN,
      personalScoreChange:""
    }
  },
  watch:{
    personalScore:{
      deep:true,
      handler:function (newValue,oldVal){
        console.log("just do it")
        this.personalScoreChange=newValue
      }
    },
  },
  methods:{
    addShow(index) {
      this.index=index
      //显示弹窗
      this.dialogFormVisible = true;
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
    },
    addDo(){
      this.personalScore[this.index-1].score=parseFloat(this.point)
      this.dialogFormVisible = false;
      axios.post("/teacher_api/personal_score", {
        key:this.personalScore[this.index-1].key,
        score:this.personalScore[this.index-1].score
      },{
        headers: {
          "X-CSRFToken": document.cookie.split("=")[1],
        }}).then((res)=>{
      })
      this.point=undefined
    },
  }
}
</script>

<style scoped>
</style>
