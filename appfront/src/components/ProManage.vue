<template>
  <div class="ProManage">
    <el-container class="all-background">
      <el-header style="text-align: left; font-size: 20px; color: #ffff">
        <el-row style="margin: auto 5%;">
          <teacher-head-line v-bind:id="this.$route.params.tid"></teacher-head-line>
        </el-row>
      </el-header>

      <el-container>

        <el-tabs :tab-position="tabPosition" style="height: 800px; min-width: 98%;" type="border-card"
                 v-model="activename">
          <el-tab-pane label="日历" name="1">
            <el-calendar>
              <!-- 这里使用的是 2.5 slot 语法，对于新项目请使用 2.6 slot 语法-->
              <template slot="dateCell" slot-scope="{date, data}">
                <p :class="data.isSelected ? 'is-selected' : ''">
                  {{ data.day.split('-').slice(1).join('-') }} {{ data.isSelected ? '✔️' : ''}}
                </p>

              </template>
            </el-calendar>
          </el-tab-pane>
          <br>
          <el-tab-pane label="小组管理" name="2">
            <el-container>
              <el-tabs class="tabs2" type="card">
                <el-tab-pane v-for="(clas, index) in classes"
                             :key="index" :label="clas.title">
                   <el-container>
                     <el-button style=" margin-left: 120px; margin-bottom: 10px;" @click="download(clas.id)">下载组队信息</el-button>
                     <el-button style=" margin-bottom: 10px;" @click="send3(clas.id)">一键提醒</el-button>
                   </el-container>

                  <el-container>
                    <template>
                      <el-table :data="clas.groupData" height="600px" border style="width: 100%; margin-left: 120px; margin-top: 5px;">
                        <el-table-column fixed prop="groupid" label="编号" width="150">
                        </el-table-column>
                        <el-table-column prop="pro" label="项目" width="150">
                        </el-table-column>
                        <el-table-column prop="leader" label="队长" width="150">
                        </el-table-column>
                        <el-table-column prop="member" label="成员" width="400">
                        </el-table-column>
                        <el-table-column prop="lab" label="实验班" width="100">
                        </el-table-column>
                        <el-table-column fixed="right" label="操作" width="150">
                          <template slot-scope="scope">
                            <el-button @click="look(index, scope.$index)" type="text" size="small">查看</el-button>
                            <el-button @click="lookup(index, scope.$index)" type="text" size="small">评分</el-button>
                            <el-popover
                              placement="right"
                              style="width: auto;"
                              trigger="click">
                              <el-input v-model="input" placeholder="请输入信息" type="textarea" :rows="2"
                                        clearable></el-input>
                              <el-button type="text" size="medium" style="margin-left: 80%;"
                                         @click="send2(input, clas.id, scope.$index)">确认
                              </el-button>

                              <el-button slot="reference" type="text" size="small" @click="empty">提醒</el-button>
                            </el-popover>
                          </template>
                        </el-table-column>
                      </el-table>
                    </template>
                  </el-container>
                </el-tab-pane>
              </el-tabs>
            </el-container>
          </el-tab-pane>
          <br>
          <el-tab-pane label="学生管理" name="3">
            <el-container class="trans">
              <el-tabs class="tabs" type="card" style="min-width: 95%;width: 1200px;">
                <el-tab-pane v-for="(clas, index) in classes"
                             :key="clas" :label="clas.title"  >
                  <el-container class="trans">
                    <template>
                      <el-transfer filterable :filter-method="filterMethod" filter-placeholder="请输入学号"
                                   :titles="['学生列表', '操作框']"
                                   :props="{key: 'ikey'}" v-model="clas.value" :data="clas.studentlist"
                                   style="margin-left: 100px;">
                        <el-button @click="send(input, clas.id)" class="transfer-footer" slot="left-footer" size="small"
                                   style="margin-left: 8px;">全体通知
                        </el-button>
                        <el-button @click="findstu(clas.id)" class="transfer-footer" slot="left-footer" size="small"
                                   style="margin-left: 8px;">筛选未组队学生
                        </el-button>
                        <el-button @click="sendmsg(input, clas.id)" class="transfer-footer" slot="right-footer"
                                   size="small" style="margin-left: 8px;">发送消息
                        </el-button>
                        <el-button @click="SA(clas.id)" class="transfer-footer" slot="right-footer" size="small"
                                   style="margin-left: 8px;">任命为助教
                        </el-button>
                        <el-button @click="noSA(clas.id)" class="transfer-footer" slot="right-footer" size="small"
                                   style="margin-left: 8px;">取消助教资格
                        </el-button>
                      </el-transfer>
                    </template>
                  </el-container>
                  <el-input v-model="input" placeholder="请输入信息"
                            style="margin-left: 200px; margin-top: 30px; width: 600px;" clearable></el-input>
                </el-tab-pane>
              </el-tabs>
            </el-container>
          </el-tab-pane>
          <br>
          <el-tab-pane label="项目管理" name="4">
            <el-container>
              <el-dialog
                title="重设答辩时间"
                :visible.sync="Visible"
                width="35%"
                center
                append-to-body
              >
                <el-form label-width="80px">
                  <el-form-item v-for="(dates, index) in date2"
                                :key="index" label="答辩信息">
                    <el-select v-model="dates.prelistid" placeholder="第？次答辩" style="width: 120px;">
                      <el-option label="1" value="1"></el-option>
                      <el-option label="2" value="2"></el-option>
                      <el-option label="3" value="3"></el-option>
                      <el-option label="4" value="4"></el-option>
                      <el-option label="5" value="5"></el-option>
                      <el-option label="6" value="6"></el-option>
                    </el-select>
                    <br>
                    <el-date-picker
                      type="datetimerange"
                      range-separator="至"
                      start-placeholder="开始日期"
                      end-placeholder="结束日期" v-model="dates.tim"
                      value-format="yyyy-MM-dd HH:mm:ss"
                      style="width: 400px; margin-top: 5px;"></el-date-picker>
                    <br>
                    <el-input v-model="dates.timelimit" placeholder="答辩时间限制/min" type="text"
                              style="width: 200px; margin-top: 5px;" clearable></el-input>
                  </el-form-item>
                  <el-button @click="addTime" size="mini" style="margin-left: 100px; margin-bottom: 15px;">添加答辩信息
                  </el-button>
                  <el-button @click="deleteTime" size="mini" style="margin-left: 40px; margin-bottom: 15px;">删除答辩信息
                  </el-button>
                </el-form>
                <el-button @click="refresh2">取 消</el-button>
                <el-button type="primary" @click="onSubmit2">确 定</el-button>
              </el-dialog>
              <el-dialog
                title="创建新项目"
                :visible.sync="centerDialogVisible"
                width="50%"
                center
                append-to-body
              >
                <el-form ref="form" :model="form" label-width="130px">
                  <el-form-item label="课程第？次项目">
                    <el-input v-model="form.number" placeholder="请输入项目序号" type="text" style="width: 200px;"
                              clearable></el-input>
                  </el-form-item>
                  <el-form-item label="项目名称">
                    <el-input v-model="form.name" placeholder="请输入项目名" type="text" style="width: 200px;"
                              clearable></el-input>
                  </el-form-item>
                  <el-form-item label="项目分类">
                    <el-input v-model="form.categorize" placeholder="请输入项目分类" type="text" style="width: 200px;"
                              clearable></el-input>
                  </el-form-item>
                  <el-form-item label="小组最小人数">
                    <el-select v-model="form.minnum" placeholder="请选择人数" style="width: 200px;">
                      <el-option label="1" value="1"></el-option>

                      <el-option label="2" value="2"></el-option>

                      <el-option label="3" value="3"></el-option>

                      <el-option label="4" value="4"></el-option>

                      <el-option label="5" value="5"></el-option>

                      <el-option label="6" value="6"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="小组最大人数">
                    <el-select v-model="form.maxnum" placeholder="请选择人数" style="width: 200px;">
                      <el-option label="1" value="1"></el-option>

                      <el-option label="2" value="2"></el-option>

                      <el-option label="3" value="3"></el-option>

                      <el-option label="4" value="4"></el-option>

                      <el-option label="5" value="5"></el-option>

                      <el-option label="6" value="6"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="截止日期">
                    <el-date-picker type="datetime" placeholder="选择日期时间" v-model="form.date1"
                                    format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                                    style="width: 200px;"></el-date-picker>
                  </el-form-item>
                  <el-form-item v-for="(dates, index) in date2"
                                :key="index" label="答辩信息">
                    <el-select v-model="dates.prelistid" placeholder="第？次答辩" style="width: 120px;">
                      <el-option label="1" value="1"></el-option>
                      <el-option label="2" value="2"></el-option>
                      <el-option label="3" value="3"></el-option>
                      <el-option label="4" value="4"></el-option>
                      <el-option label="5" value="5"></el-option>
                      <el-option label="6" value="6"></el-option>
                    </el-select>
                    <br>
                    <el-date-picker
                      type="datetimerange"
                      range-separator="至"
                      start-placeholder="开始日期"
                      end-placeholder="结束日期" v-model="dates.tim"
                      value-format="yyyy-MM-dd HH:mm:ss"
                      style="width: 400px; margin-top: 5px;"></el-date-picker>
                    <br>
                    <el-input v-model="dates.timelimit" placeholder="答辩时间限制/min" type="text" style="width: 200px;"
                              clearable></el-input>
                  </el-form-item>
                  <el-button @click="addTime" size="mini" style="margin-left: 100px; margin-bottom: 15px;">添加答辩信息
                  </el-button>
                  <el-button @click="deleteTime" size="mini" style="margin-left: 40px; margin-bottom: 15px;">删除答辩信息
                  </el-button>
                  <el-form-item label="是否允许跨班组队">
                    <el-select v-model="form.across" placeholder="请选择" style="width: 100px;">
                      <el-option label="是" value="true"></el-option>
                      <el-option label="否" value="false"></el-option>
                    </el-select>
                  </el-form-item>
                </el-form>

                <el-button @click="refresh">取 消</el-button>
                <el-button type="primary" @click="onSubmit">确 定</el-button>

              </el-dialog>
              <el-tabs class="tabs3" type="card">
                <el-tab-pane v-for="(clas, index) in classes"
                             :key="index" :label="clas.title" style="height: 100%;">
                  <el-button  @click="DialogVisible(index)" style="margin-left: 90%; margin-bottom: 5px;">添加项目</el-button>


                  <el-container>
                    <template>
                      <el-table :data="clas.prodata" height="600px" border style=" margin-left: 5px; width: 60%;">
                        <el-table-column prop="proindex" label="项目序号" width="80">
                        </el-table-column>
                        <el-table-column prop="pro2" label="项目名称" width="100">
                        </el-table-column>
                        <el-table-column prop="number" label="队数" width="60">
                        </el-table-column>
                        <el-table-column label="答辩日期" width="290">
                          <template slot-scope="scope">
                            <el-table :data="clas.prodata[scope.$index].prelist">
                              <el-table-column prop="presentationid" label="答辩序号" width="80">
                              </el-table-column>
                              <el-table-column prop="presentationtime" label="答辩时间" width="210">
                              </el-table-column>
                            </el-table>
                          </template>
                        </el-table-column>
                        <el-table-column prop="time" label="截止期" width="160">
                        </el-table-column>
                        <el-table-column label="重设截止期" width="280">
                          <template slot-scope="scope">
                            <el-date-picker type="datetime" placeholder="选择日期时间" v-model="value1[scope.$index]"
                                            format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                                            style="width: 200px;"></el-date-picker>
                            <el-button @click="change(clas.id, scope.$index, value1[scope.$index])" type="text"
                                       size="small">确定
                            </el-button>
                          </template>
                        </el-table-column>
                        <el-table-column label="重设答辩信息" >
                          <template slot-scope="scope">
                            <el-button @click="dialog(index, scope.$index)" type="text" size="small">操作</el-button>
                          </template>
                        </el-table-column>
                        <el-table-column label="删除项目" width="80">
                          <template slot-scope="scope">
                            <el-button @click="deletepro(index, scope.$index)" type="text" size="small">确认删除</el-button>
                          </template>
                        </el-table-column>
                        <el-table-column label="创建评分模板" >
                          <el-button @click="template" type="text" size="small">创建</el-button>
                        </el-table-column>
                        <el-table-column label="一键组队">
                          <template slot-scope="scope">
                            <el-button @click="group(index, scope.$index)" type="text" size="small">半随机</el-button>
                          </template>
                        </el-table-column>
                      </el-table>
                    </template>
                  </el-container>
                </el-tab-pane>
              </el-tabs>
            </el-container>
          </el-tab-pane>
        </el-tabs>
      </el-container>
    </el-container>
  </div>
</template>

<script>
    import axios from "axios";
    import TeacherHeadLine from "./TeacherHeadLine";

    export default {
        components: {TeacherHeadLine},
        data() {

            return {
                classes: [
                    {
                        id: "",
                        title: "",
                        studentlist: [
                            {
                                label: '',
                                ikey: undefined,
                                ids: '',
                                isgroup: undefined,
                            }
                        ],
                        value: [],
                        groupData: [{
                            groupid: '',
                            pro: '',
                            leader: '',
                            member: '',
                            state: '',
                            lab: '',
                            groupkey: undefined,
                          },
                        ],
                        prodata: [{
                            id2: '',
                            pro2: '',
                            number: '',
                            prelist: [
                                {
                                    presentationid: undefined,
                                    presentationkey: undefined,
                                    presentationname: "",
                                    presentationtime: [
                                    ]
                                },
                            ],

                            time: '',
                            proindex: undefined,
                            prokey: undefined,
                        },
                        ],
                    },
                ],

                value1: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',],
                filterMethod(query, item) {
                    return item.ids.indexOf(query) > -1;
                },
                input: '',
                idx: -1,
                idx2: -1,
                form: {
                    number: '',
                    name: '',
                    maxnum: '',
                    minnum: '',
                    date1: '',
                    across: '',
                    categorize: '',
                },
                date2: [
                    {
                        prelistid: '',
                        tim: '',
                        timelimit: '',
                    },
                ],

                rules: {
                    number: [
                        {required: true, message: '请输入项目序号', trigger: 'blur'},
                    ],
                    name: [
                        {required: true, message: '请输入项目名称', trigger: 'blur'}
                    ],
                    num: [
                        {required: true, message: '请选择小组人数', trigger: 'change'}
                    ],
                },
                Visible: false,
                centerDialogVisible: false,
                tabPosition: "left",
                cindex: 0,
                teacher: this.$route.params.tid,
                activename: this.$route.query.aname,
                dateture: false,
            }
        },

        created() {
            this.teacher = this.$route.params.tid;
            this.activename = this.$route.query.aname;
            console.log(this.teacher);
            console.log(this.activename);
            axios.post("/teacher_api/promanage", {teacherid: this.teacher,},
            {
                headers: {
                    'X-CSRFToken': document.cookie.split("=")[1]
                }
            }
            )
                .then((res) => {
                    if (res.data.status === 200) {
                        this.classes = res.data.class;
                    }
                    this.reload();
                });
        },
        methods: {
            refresh() {
                this.centerDialogVisible = false;
            },
            refresh2() {
                this.Visible = false;
            },
            dialog(index, index2) {
                this.idx = index;
                this.idx2 = index2;
                console.log(this.idx);
                console.log(this.idx2);
                console.log(this.Visible);
                this.Visible = true;
                console.log(this.Visible);
                this.renew();
            },
            DialogVisible(index) {
                this.idx = index;
                console.log(index);
                console.log(this.centerDialogVisible);
                this.centerDialogVisible = true;
                console.log(this.centerDialogVisible);
                this.renew();
            },
            change(classid, index, str) {
                this.value1 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',],
                    console.log(str);
                for (let i in this.classes) {
                    if (this.classes[i].id === classid) {
                        this.cindex = i;
                    }
                }
                ;

                if(str==''){
                  this.$message('请选择新的截止期');
                }else{
                  console.log(classid);
                  console.log(this.cindex);
                  this.classes[this.cindex].prodata[index].time = str;
                  console.log(this.classes[this.cindex].prodata[index].time);
                  axios.post("/teacher_api/alter_ddl", {
                    teacherid: this.teacher,
                      prokey: this.classes[this.cindex].prodata[index].prokey,
                      date: str,
                  }, {
                      headers: {
                          'X-CSRFToken': document.cookie.split("=")[1]
                      }
                  })
                      .then((res) => {
                          if (res.data.status === 200) {
                              this.$message(res.data.msg);
                              this.classes=res.data.class;
                          }else{
                            this.$message(res.data.msg);
                          }
                      });
                }

            },
            addTime() {
                this.date2.push(
                    {
                        prelistid: '',
                        tim: '',
                        timelimit: '',
                    }
                );
            },
            deleteTime() {
                this.date2.splice(this.date2.length - 1, 1);
            },
            onSubmit() {
                console.log(this.idx)
                console.log(this.centerDialogVisible);

                if (this.form.number === '') {
                    this.$message('请输入项目序号');
                } else if (this.form.name === '') {
                    this.$message('请输入项目名称');
                }else if(this.form.categorize===''){
                  this.$message('请输入项目分类');
                }else if (this.form.minnum === '') {
                    this.$message('请选择小队最小人数');
                } else if(this.form.maxnum == ''){
                   this.$message('请选择小队最大人数');
                }else {
                    console.log(this.centerDialogVisible);
                    this.centerDialogVisible = false;
                    console.log(this.centerDialogVisible);
                    axios.post("/teacher_api/create_project", {
                        teacherid: this.teacher,
                        classid: this.classes[this.idx].id,
                        project_name: this.form.name,
                        prelist: this.date2,
                        project_deadline: this.form.date1,
                        maxsize: this.form.maxnum,
                        minsize: this.form.minnum,
                        proindex: this.form.number,
                        across: this.form.across,
                        categorize: this.form.categorize,
                    }, {
                        headers: {
                            'X-CSRFToken': document.cookie.split("=")[1]
                        }
                    })
                        .then((res) => {
                            if (res.data.status === 200) {
                              this.$message('创建成功');
                                this.classes = res.data.class;

                            }else{
                              this.$message(res.data.msg);
                            }
                        });
                }
            },
            onSubmit2() {
              console.log(this.date2)
              for (let i in this.date2){
                if(this.date2[i].prelistid=='' || this.date2[i].tim=='' || this.date2[i].timelimit==''){
                  console.log(this.dateture);
                  this.dateture=true;
                  console.log(this.dateture);
                }
              };
                if(this.dateture){
                  this.$message('请输入完整答辩信息');
                  console.log(this.dateture);
                  this.dateture=false;
                  console.log(this.dateture);
                }else{
                  console.log(this.Visible);
                  this.Visible = false;
                  console.log(this.Visible);
                  console.log(this.classes[this.idx].prodata[this.idx2].prokey);
                  axios.post("/teacher_api/alter_presentation", {
                      teacherid: this.teacher,
                      prelist: this.date2,
                      prokey: this.classes[this.idx].prodata[this.idx2].prokey,
                  }, {
                      headers: {
                          'X-CSRFToken': document.cookie.split("=")[1]
                      }
                  })
                      .then((res) => {
                          console.log(res)
                          if (res.data.status === 200) {
                            this.$message('更新成功');
                              this.classes = res.data.class;
                          }else{
                            this.$message(res.data.msg);
                          }
                      });
                }

            },
            deletepro(index, index2){
              console.log(this.classes[index].prodata[index2].prokey);
              axios.post("/teacher_api/delete_project", {
                  teacherid: this.teacher,
                  prokey: this.classes[index].prodata[index2].prokey,
              }, {
                  headers: {
                      'X-CSRFToken': document.cookie.split("=")[1]
                  }
              })
                  .then((res) => {
                      console.log(res)
                      if (res.data.status === 200) {
                        this.$message('删除成功');
                          this.classes = res.data.class;
                      }else{
                        this.$message(res.data.msg);
                      }
                  });
            },
            group(index, index2){
              console.log(this.classes[index].prodata[index2].prokey);
                axios.post("/teacher_api/auto_group", {
                    teacherid: this.teacher,
                    prokey: this.classes[index].prodata[index2].prokey,
                }, {
                    headers: {
                        'X-CSRFToken': document.cookie.split("=")[1]
                    }
                })
                    .then((res) => {
                        console.log(res)
                        if (res.data.status === 200) {
                          this.$message('随机组队成功');
                        }else{
                          this.$message(res.data.msg);
                        }
                    });

            },
            send(str, classid) {
                this.input = "";
                for (let i in this.classes) {
                    if (this.classes[i].id == classid) {
                        this.cindex = i;
                    }
                }
                ;
                console.log(this.cindex);
                console.log(str);
                if(str == ''){
                  this.$message('请不要输入空白信息！');
                }else{
                  axios.post("/teacher_api/send_to_class", {
                      teacherid: this.teacher,
                      classid: classid,
                      content: str,
                      sendtime: this.getTime(),

                  }, {
                      headers: {
                          'X-CSRFToken': document.cookie.split("=")[1]
                      }
                  })
                      .then((res) => {

                          if (res.data.status === 200) {
                              this.$message(res.data.msg);
                          }else{
                            this.$message(res.data.msg);
                          }
                      });
                }

            },
            findstu(classid){
              for (let i in this.classes) {
                  if (this.classes[i].id == classid) {
                      this.cindex = i;
                  }
              };
              console.log(this.cindex);
              for(let i in this.classes[this.cindex].studentlist){
                if(!this.classes[this.cindex].studentlist[i].isgroup){
                  this.classes[this.cindex].value.push(this.classes[this.cindex].studentlist[i].ikey);
                }
              };
            },
            sendmsg(str, classid) {
                this.input = "";
                for (let i in this.classes) {
                    if (this.classes[i].id == classid) {
                        this.cindex = i;
                    }
                }
                ;
                console.log(this.cindex);
                console.log(str);
                for (let i in this.classes[this.cindex].value) {
                    console.log(this.classes[this.cindex].value[i]);
                }
                ;
                if(str == ''){
                  this.$message('请不要输入空白信息');
                }else{
                  axios.post("/teacher_api/send_to_stu", {
                      teacherid: this.teacher,
                      classid: classid,
                      stuid: this.classes[this.cindex].value,
                      content: str,
                      sendtime: this.getTime(),

                  }, {
                      headers: {
                          'X-CSRFToken': document.cookie.split("=")[1]
                      }
                  })
                      .then((res) => {
                          if (res.data.status === 200) {
                              this.$message(res.data.msg);
                          }else{
                            this.$message(res.data.msg);
                          }
                      });
                }
            },
            SA(classid) {
                this.input = "";
                for (let i in this.classes) {
                    if (this.classes[i].id == classid) {
                        this.cindex = i;
                    }
                }
                ;
                console.log(classid);
                console.log(this.cindex);
                axios.post("/teacher_api/set_sa", {
                    classid: classid,
                    stuid: this.classes[this.cindex].value,
                    operate: 'SA',
                }, {
                    headers: {
                        'X-CSRFToken': document.cookie.split("=")[1]
                    }
                })
                    .then((res) => {
                        if (res.data.status === 200) {
                            this.$message(res.data.msg);
                        }else{
                          this.$message(res.data.msg);
                        }
                    });
            },
            noSA(classid) {
                this.input = "";
                for (let i in this.classes) {
                    if (this.classes[i].id == classid) {
                        this.cindex = i;
                    }
                }
                ;
                console.log(this.cindex);
                axios.post("/teacher_api/set_sa", {
                    classid: classid,
                    stuid: this.classes[this.cindex].value,
                    operate: 'stu',
                }, {
                    headers: {
                        'X-CSRFToken': document.cookie.split("=")[1]
                    }
                })
                    .then((res) => {
                        if (res.data.status === 200) {
                            this.$message(res.data.msg);
                        }else{
                          this.$message(res.data.msg);
                        }
                    });
            },
            send2(str, classid, index) {
                this.input = "";
                for (let i in this.classes) {
                    if (this.classes[i].id == classid) {
                        this.cindex = i;
                    }
                }
                ;
                console.log(this.cindex);
                console.log(index);
                console.log(this.classes[this.cindex].groupData[index].groupid);
                console.log(str);
                console.log(this.getTime());
                axios.post("/teacher_api/send_to_group", {
                    teacherid: this.teacher,
                    groupid: this.classes[this.cindex].groupData[index].groupkey,
                    content: str,
                    sendtime: this.getTime(),

                }, {
                    headers: {
                        'X-CSRFToken': document.cookie.split("=")[1]
                    }
                })
                    .then((res) => {
                        if (res.data.status === 200) {
                            this.$message(res.data.msg);
                        }else{
                          this.$message(res.data.msg);
                        }
                    });
            },
            send3(classid) {
                axios.post("/teacher_api/send_to_class", {
                    teacherid: this.teacher,
                    classid: classid,
                    content: "请尽快完成项目并确定答辩时间",
                    sendtime: this.getTime(),

                }, {
                    headers: {
                        'X-CSRFToken': document.cookie.split("=")[1]
                    }
                })
                    .then((res) => {
                        if (res.data.status === 200) {
                            this.$message(res.data.msg);
                        }else{
                          this.$message(res.data.msg);
                        }
                    });
            },
            download(clssid){
              axios({
                        methods: "get",
                        url:"/student_api/download_group",
                        params:{
                          teacherid: this.teacher,
                          classid: classid,
                        },
                        responseType:"blob"
                      }).then(res => {
                        let blob = new Blob([res.data
                        ]);
                        let downloadElement = document.createElement("a");
                        let href = window.URL.createObjectURL(blob); //创建下载的链接
                        downloadElement.href = href;
                        downloadElement.download = file.name; //下载后文件名
                        document.body.appendChild(downloadElement);
                        downloadElement.click(); //点击下载
                        document.body.removeChild(downloadElement); //下载完成移除元素
                        window.URL.revokeObjectURL(href); //释放掉blob对象
                      });
            },
            look(index, index2) {

                console.log(index);
                console.log('da');
                console.log(index2);
                console.log('da');
                console.log(this.classes[index].groupData[index2].groupkey);
                console.log('da');
                // for (let i in this.classes[this.cindex].groupData){
                //   console.log(this.classes[this.cindex].groupData[index].groupid);
                // };
                let groupId = this.classes[index].groupData[index2].groupkey
                let jump = document.createElement("a")
                jump.href = '/team/' + groupId + '?qtid=' + this.teacher
                jump.click()
                document.body.removeChild(jump)
            },
            lookup(index, index2) {

                console.log(index);
                console.log('da');
                console.log(index2);
                console.log('da');
                console.log(this.classes[index].groupData[index2].groupkey);
                console.log('da');
                // for (let i in this.classes[this.cindex].groupData){
                //   console.log(this.classes[this.cindex].groupData[index].groupid);
                // };
                let groupId = this.classes[index].groupData[index2].groupkey
                let jump = document.createElement("a")
                jump.href = '/groupMark/' + groupId + '?qtid=' + this.teacher
                jump.click()
                document.body.removeChild(jump)
            },
            empty() {
                this.input = "";
            },
            getTime() {
                var dat = new Date();
                var year = dat.getFullYear();
                var month = dat.getMonth() + 1;
                var day = dat.getDate();
                var hours = dat.getHours();
                var minutes = dat.getMinutes();
                var seconds = dat.getSeconds();
                return year + "年" + month + "月" + day + "日" + hours + ":" + minutes + ":" + seconds
            },
            renew(){
              this.date2 = [{prelistid: '', tim: '', timelimit: '',},]
              this.form = {
                    number: '',
                    name: '',
                    maxnum: '',
                    minnum: '',
                    date1: '',
                    across: '',
                    categorize: '',
                };
            },
            template(){
              let jump = document.createElement("a")
              jump.href = '/mt?qtid=' + this.teacher
              jump.click()
              document.body.removeChild(jump)
            },
        },
    }
</script>

<style>
  .ProManage {
    background-color: #ffffff;
    top: 0px;
    left: 0px;
    right: 0px;
    position: absolute;
    min-height: 100%;
  }

  .el-header {
    background-color: #ffffff;
    background-size: 100% 100%;
    top: 0px;
    left: 0px;
    right: 0px;
    bottom: 0px;
    line-height: 70px;
    border-style: window-inset;
    border-color: #000000;
  }

  .ProManage {
    top: 0px;
  }



  .el-transfer-panel__list.is-filterable {

    height: 500px;
  }

  .tabs {
    top: -57px;
    position: relative;
  }

  .tabs2 {
    top: -36px;
    position: relative;
  }

  .tabs3 {
    top: -78px;

    position: relative;
  }
  .trans{
    width: 1200px;
    min-width: 1200px;
  }

</style>
