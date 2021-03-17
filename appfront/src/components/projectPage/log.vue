<template>

  <div id="log">
    <el-row>
      <div v-for="(log,index) in logs"  :key="index" style="line-height: 10px">
        <el-card>
          <span style="font-size: 20px">
            <el-form label-width="20%" class="spHeight">
              <el-form-item label="传输人" >
                <el-col >{{ log.sender }}</el-col>
              </el-form-item>
              <el-form-item label="传输时间" >
                <el-col >{{ log.time }}</el-col>
              </el-form-item>
              <el-form-item label="操作类型" >
                <el-col >{{ log.operation }}</el-col>
              </el-form-item>
              <el-form-item label="操作文件" >
                <el-col >{{ log.fileName }}</el-col>
              </el-form-item>
            </el-form>
          </span>
        </el-card>
      </div>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "log",
  props:["logs"],
  data(){
    return{
    }
  },

  methods:{
    click(){
      this.$forceUpdate()
      console.log(this.logs)
    },
  }
}
</script>

<style scoped>
.spHeight>>>label{
  line-height: 20px;
}
.spHeight>>input{
  line-height: 30px;
}
.el-col{
  line-height: 20px;
}
</style>
