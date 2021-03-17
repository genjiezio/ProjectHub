<template>
  <div id="presentation" style="line-height: 35px">
    <br>
    <el-row>
      <el-col span="8">
        <span style="display: inline-block; font-size: 20px">答辩日期:</span>
      </el-col>
      <el-col span="12">
        <span v-if="SA">
          {{teacherGetDate()}}
        </span>
        <span v-else-if="this.$route.query.qsid!==undefined">
          <el-select v-model="date" :placeholder="this.getDate()"  @focus="this.checkArray" @change="this.clearTime">
          <el-option
            v-for="item in presentation"
            :key="item[0]"
            :value="item[0]"
            :disabled="item.disabled">
          </el-option>
        </el-select>
        </span>
        <span v-if="this.$route.query.qtid!==undefined" style="font-size: 20px">
          <span>{{teacherGetDate()}}</span>
        </span>
      </el-col>
    </el-row>
    <br>
    <el-row>
      <el-col span="8">
        <span style="display: inline-block; font-size: 20px">答辩时间:</span>
      </el-col>
      <el-col span="12">
        <span v-if="SA">
          {{teacherGetTime()}}
        </span>
        <span v-else-if="this.$route.query.qsid!==undefined">
          <el-select v-model="time" :placeholder="this.getTime()" @focus="this.checkDate" @change="this.updateTime">
          <el-option
            v-for="item in this.timeArray"
            :key="'from '+item[0]+' to '+item[1]"
            :value="'from '+item[0]+' to '+item[1]"
            :disabled="item[2]">
          </el-option>
        </el-select>
        </span>
        <span v-if="this.$route.query.qtid!==undefined" style="font-size: 20px">
          {{teacherGetTime()}}
        </span>
      </el-col>
    </el-row>

  </div>

</template>

<script>
import axios from "axios"
export default {
  name: "presentation",
  props:["presentation","groupId","studentId","chooseTime","SA"],
  data() {
    return {
      date: '',
      time: '',
      timeArray:[],
      presentationChange:[],
      chooseTimeChange:[],
    }
  },
  methods:{
    checkDate(){
      let idx=-1
      if(this.presentation){
        for(let i=0;i<this.presentation.length;i++){
          if(this.presentation[i][0]===this.date){
            idx = i
          }
        }
      }
      if (idx===-1){
        alert("The date is illegal, please choose a new one.")
      }
      else{
        this.timeArray=this.presentation[idx][1]
      }
    },
    checkArray(){
      if(this.presentation){
        if(this.presentation.length===0){
          alert("The presentation still not public")
        }
      }
    },
    clearTime(){
      this.time=''
    },
    updateTime(){
      if(this.time!==''){
        let arr= this.time.split(' ')
        let id=-1
        if(this.presentation){
          for(let i=0;i<this.presentation.length;i++){
            if(this.presentation[i][0]===this.date){
              if(this.presentation[i][1]){
                for(let k=0;k<this.presentation[i][1].length;k++){
                  if(this.presentation[i][1][k][0]===arr[1]){
                    id=this.presentation[i][1][k][3]
                  }
                }
              }
            }
          }
        }
        axios.post('/student_api/choose_time',{
          timeId:id,
          groupId:this.$route.params.gid
        },{
          headers: {
            "X-CSRFToken": document.cookie.split("=")[1],
          }}).then((res)=>{
          this.$message(res.data.status+":"+res.data.msg
          )
        })
      }
    },
    getDate(){
      if (this.chooseTime){
        if(this.chooseTime.length===3){
          return this.chooseTime[0]
        }
        else {
          return '请选择答辩日期'
        }
      }
    },
    teacherGetDate(){
      if(this.getDate()==='请选择答辩日期'){
        return "尚未选择"
      }
      else {
        return this.getDate()
      }
    },
    teacherGetTime(){
      if(this.getTime()==='请选择答辩时间'){
        return "尚未选择"
      }
      else {
        return this.getTime()
      }
    },
    getTime(){
      if (this.chooseTime){
        if(this.chooseTime.length===3){
          return 'from '+this.chooseTime[1]+' to '+this.chooseTime[2]
        }
        else {
          return '请选择答辩时间'
        }
      }
    }
  },
  created(){
    this.dataRefresh();
  },
  watch:{
    presentation:{
      deep:true,
      handler:function (newValue,oldVal){
        this.presentationChange=newValue
      }
    },
    chooseTime:{
      deep:true,
      handler:function (newValue,oldVal){
        this.chooseTimeChange=newValue
      }
    }
  },
}
</script>

<style scoped>
</style>
