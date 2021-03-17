<template>
  <div class="HomePage">
    <div class="HomePage-wrap">
      <el-container class="all-background">
      <el-header style="text-align: left; font-size: 20px; color: #ffff">
        <el-row style="margin: auto 5%;">
          <HeadLine v-bind:id="$route.params.sid"></HeadLine>
        </el-row>
      </el-header>
      <el-container style="border: 1px solid #eee">
        <el-aside width="400px" style="background-color: rgb(255, 255, 255)">
          <el-menu router :default-openeds="['1', '3']">
            <el-submenu index="1">
              <template slot="title"
                ><i class="el-icon-more-outline"></i>正在参加的项目</template
              >
              <el-menu-item
                v-for="(todo, index) in info.todos"
                :key="index"
                style="color: #1989fa"
              >
                <el-button
                 :disabled="showits(todo.SA)"
                  @click="choosePage(todo.groupid)"
                  style="border: none; color: #1989fa; margin-left: 30px"
                  type="text"
                  >{{ todo.title }}</el-button
                >

                <el-tag
                  type="success"
                  size="mini"
                  style="margin-left: 5px; margin-top: 1px"
                >
                  {{ todo.class+' '+todo.lab}}
                </el-tag>
                <el-button
                  :disabled="showit(todo.SA)"
                  @click="findsa(todo.id)"
                  style="
                    border: none;
                    color: #aaa1aa;
                    float: right;
                    margin-top: 6px;
                  "
                  type="text"
                  >管理</el-button
                >
              </el-menu-item>
            </el-submenu>

            <el-submenu index="2">
              <template slot="title"
                ><i class="el-icon-more-outline"></i>已完成的项目</template
              >
              <el-menu-item
                v-for="(done, index) in info.dones"
                :key="index"
                style="color: #1989fa"
              >
                <el-button
                  @click="choosePage(done.id)"
                  style="border: none; color: #1989fa; margin-left: 30px"
                  type="text"
                  >{{ done.title }}</el-button
                >

                <el-tag
                  type="success"
                  size="mini"
                  style="margin-left: 5px; margin-top: 1px"
                >
                  {{ done.class+' '+done.lab}}
                </el-tag>
              </el-menu-item>
            </el-submenu>
            <el-submenu index="3">
              <template slot="title"
                ><i class="el-icon-more-outline"></i>参加项目</template
              >
              <el-menu-item
                v-for="(pro, index) in info.prodata"
                :key="index"
                style="color: #1989fa"
              >
                <el-button
                @click="findpro(pro.id)"
                  style="border: none; color: #1989fa; margin-left: 30px"
                  type="text"
                  >{{ pro.title }}</el-button
                >
              </el-menu-item>
              >
            </el-submenu>

          </el-menu>
          </el-aside>

        <el-main>
          <el-calendar v-model="timevalue" id="calendar">
                <!-- 这里使用的是 2.5 slot 语法，对于新项目请使用 2.6 slot 语法-->
                <template
                 slot="dateCell"
                 slot-scope="{date, data}">
                  <!--自定义内容-->
                    <div>
                       <div class="calendar-day">{{ data.day.split('-').slice(2).join('-') }}</div>
                          <div v-for="item in calendarData">
                             <div v-if="(item.months).indexOf(data.day.split('-').slice(1)[0])!==-1">
                               <div v-if="(item.days).indexOf(data.day.split('-').slice(2).join('-'))!== -1">
                                    <el-tooltip class="item" effect="dark" :content="tip(item.things, item.months, item.days, item.time)" placement="left-end">
                                         <el-button style="border: none;"
                                                 type="text" class="is-selected">{{item.things}} </el-button>
                                    </el-tooltip>
                                 </div>
                              <div v-else></div>
                             </div>
                         <div v-else></div>
                       </div>
                    </div>
                </template>
          </el-calendar>
        </el-main>
      </el-container>
      </el-container>
    </div>

  </div>
</template>

<script>
import HeadLine from "./HeadLine";
import axios from "axios";
export default {
  components:{HeadLine},
  name: "HomePage",
  data() {
    return {
      drawer: false,
      disable: true,
      calendarData: [
                          {
                            months: [''],
                            days: [''],
                            things: '' ,
                            time: '',
                            },
                          { months: [''], days: [''],things: '' ,time: ''},
                          { months: [''], days: [''],things: '' ,time: ''},
                          { months: [''], days: [''],things: '' ,time: ''},
                          { months: [''], days: [''],things: '' , time: ''},
                      ],
                      timevalue: new Date(),

      info: {
        msg: "",

        todos: [
          {
            id: "",
            title: "",
            class: "",
            lab: '',
            SA: "",
            groupid: undefined,
          }
        ],
        dones: [
          {
            id: "",
            title: "",
            class: "",
            lab: '',
            groupid: undefined,
          }
        ],
        prodata: [
          {
            id: undefined,
            title: '',
          },
        ],
        sid: 2,
      },
    };
  },
  inject: ["reload"],
  created() {
      this.sid = this.$route.params.sid;
    axios.post("/student_api/get_homepage", {sid: this.sid},
    {
        headers: {
            'X-CSRFToken': document.cookie.split("=")[1]
        }
    }
    ).then((res) => {
        console.log(res)
      this.calendarData = res.data.calendarData;
      this.info.msg = res.data.msg;
      this.info.todos = res.data.todos;
      this.info.dones = res.data.dones;
      this.info.prodata = res.data.prodata;
      this.reload();
    });
  },
  methods: {
    changeInf() {
      window.location.href = "http://localhost:8086/information";
    },
    signOut() {
      window.location.href = "http://localhost:8086/login";
    },
    propage(){
      window.location.href = "http://localhost:8086/find";
    },
    choosePage(id) {
      let jump = document.createElement("a")
      jump.href = '/team/'+id+'?qsid='+this.$route.params.sid
      jump.click()
      document.body.removeChild(jump)
    },
    findpro(id){
      this.$router.push({ path: 'team/'+id+'/find', query: {qsid: this.sid} });
    },
    showit(str) {
      if (str == "true") {
        return true;
      } else {
        return false;
      }
    },
    showits(str) {
      if (str == "false") {
        return true;
      } else {
        return false;
      }
    },
    tip(str1, str2, str3, str4){
      return str1+'的提交即将于'+str2+'月'+str3+'日'+str4+'截至，请尽快完成并上传！';
    },
    findsa(id){
      let jump = document.createElement("a")
      jump.href = '/team/'+id+'?qsid='+this.$route.params.sid
      jump.click()
      document.body.removeChild(jump)
    },
  },
};
</script>

<style>
.HomePage {
  background-color: #ffffff;
  top: 0px;
  left: 0px;
  right: 0px;
  position: absolute;
  min-height: 100%;
}

.all-background {
  background-color: #f7f7f7;
  top: 0px;
  left: 0px;
  right: 0px;
  position: absolute;
  min-height: 110%;
}
.el-header {
  background-color: #ffffff;
  line-height: 60px;
}

.el-aside {
  color: #ffaaff;
}

.el-calendar-table .el-calendar-day {
  height: auto;
  min-height: 80px;

}
.calendar-day{
        text-align: center;
        color: #202535;
        line-height: 30px;
        font-size: 12px;

    }
    .is-selected{
        color: #F8A535;
        font-size: 10px;
        height: 0px;

    }
    #calendar .el-button-group>.el-button:not(:first-child):not(:last-child):after{
        content: '';
    }
</style>
