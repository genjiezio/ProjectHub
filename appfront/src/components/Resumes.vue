<template>
  <div class="resumes">
    <br>
    <el-row>
      <el-col span="4">
        颜秋阳
      </el-col>
      <el-col span="8">
        <el-progress :percentage="90"></el-progress>
      </el-col>
    </el-row>
    <br>
    <el-row>
      <el-col span="8" class="note">
        最近更新时间 : 10:10:10
      </el-col>
      <el-col span="2" class="note" push="10">
        <i class="el-icon-view">   预览</i>
      </el-col>
      <el-col span="2" class="note" push="10">
        <i class="el-icon-edit">   编辑</i>
      </el-col>
      <el-col span="2" class="note" push="10">
        <i class="el-icon-delete">   删除</i>
      </el-col>
    </el-row>
    <br>

  </div>

</template>

<script>
export default {
  name: "Resumes"
}
</script>

<style scoped>
.resumes{
  background-color: #505050;
  font-size: 18px;
}
.note{
  font-size: 14px;
}
</style>
