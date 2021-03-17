<template>
  <div class="information" >
    <br>
    <el-row >
      <el-col span="20" >
        请选择一份简历作为你的简历模板，在申请职业是快速生成投递简历，也可用于内推。
      </el-col>
      <el-col span="4">
        <el-button type="success" >新建简历</el-button>
      </el-col>
    </el-row>
    <br>
  </div>

</template>

<script>
export default {
  name: "Information"
}
</script>

<style scoped>
.information{
  background-color: #505050;
  font-size: 18px;
}
.all-background{
  background-color: #636363;
  top: 0px;
  left: 0px;
  right: 0px;
  position: absolute;
  min-height: 100%;
}
</style>
