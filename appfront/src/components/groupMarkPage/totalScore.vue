<template>
  <div id="totalScore">
    <el-row
      v-if="teamScore[0]!==calScore()">
      {{refresh()}}
    </el-row>
    <el-progress
      v-if="!isNaN(calScore())"
      :percentage="calScore()"
      :format="format"></el-progress>
    <el-alert
      v-else
      title="仍有非法分数"
      type="warning">
    </el-alert>
  </div>

</template>

<script>

import axios from "axios";

export default {
  name: "totalScore",
  props:["teamScores","teamScore"],
  methods:{
    calScore(){
      let num = 0
      if (this.teamScores){
        this.teamScores.forEach(addPoint)
      }

      function addPoint(value){
        num+=value.getScore
      }
      return num
    },
    refresh(){
      this.teamScore[0]=this.calScore()
      axios.post("/teacher_api/total_score",{
        id:this.$route.params.gid,
        totalScore:this.teamScore[0]
      },{
        headers: {
          "X-CSRFToken": document.cookie.split("=")[1],
        }}).then((res)=>{
      })
      return null
    },
    format(percentage) {
      return percentage === 100 ? '满' : `${percentage}%`;
    }
  }
}
</script>

<style scoped>

</style>
