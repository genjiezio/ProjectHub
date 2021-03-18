// pages/home/groupmy/groupmy.js
Page({

  /**
   * 页面的初始数据
   */

  data: {
    activeKey: 0,
    groupId:1,
    studentId:1,
    leaderId: 1,
    location:["README"],
    file:"../static/public/log.txt",
    projectName:"Project Helper",
    className:"CS307 OOAD",
    groupName:"group1",
    labName:"lab1",
    groupScore:90,
    personalScore:[10,11,12,13,14],
    members:[
        {
          picture:"https://csdnimg.cn/cdn/content-toolbar/csdn-logo.png?v=20200416.1",
          name:'yqy',
          studentId:0
        },
        {
          picture:"https://csdnimg.cn/cdn/content-toolbar/csdn-logo.png?v=20200416.1",
          name:'wzw',
          studentId:1
        },
        {
          picture:"https://csdnimg.cn/cdn/content-toolbar/csdn-logo.png?v=20200416.1",
          name:'zsf',
          studentId:2
        },
        {
          picture:"https://csdnimg.cn/cdn/content-toolbar/csdn-logo.png?v=20200416.1",
          name:'zcs',
          studentId:3
        },
        {
          picture:"https://csdnimg.cn/cdn/content-toolbar/csdn-logo.png?v=20200416.1",
          name:'cql',
          studentId:4
      }],
    fileList: [
        {name: 'food.jpeg',
          id: 1},
        {name: 'food2.jpeg',
        id: 2}],
    presentation:[
        ["星期一",[["10:00","10:20",true],["10:20","10:40",false],["10:40","11:00",false],["11:00","11:20",false]]],
        ["星期二",[["10:00","10:20",false],["10:20","10:40",true],["10:40","11:00",false],["11:00","11:20",false]]]
    ],
    chooseTime:["星期一","10:00","10:20"],
    logs:[
        {
          fileName:"v42e",
          sender:"yq332",
          time:"111"
        },
        {
          fileName:"vue",
          sender:"yqy",
          time:"112"
        },
    ],
    teamScores:[
        {
          id:1,
          name:"basic1",
          fullScore:20,
          getScore:1,
          text:"text"
        },
        {
          id:2,
          name:"basic2",
          fullScore:50,
          getScore:1,
          text:"text"
        },
        {
          id:3,
          name:"bonus",
          fullScore: 30,
          getScore: 1,
          text:"text"
        }
    ],
    SA:true,
    leaderName: "ss"
  },

  onChange(event) {
    this.setData({
      activeKey:event.detail,
    })
  },
  
  check(){
    return i
  },
})