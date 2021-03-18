// pages/home/grouppage/grouppage.js

var app = getApp()

Page({

  data: {
    groupList: [{
      group_name: "nn",
      group_member: ["a","b","c","d"],
      group_info: "hhhhhhhhhhhhhhhhhhhhh"
    }, {
      group_name: "nd",
      group_member: ["a","b","c","d"],
      group_info: "hhhhhhhhhhhhhhhhhhhhh"
    }]
  },

  detail(e) {
    let order = JSON.stringify(this.data.orderData[e.currentTarget.id])
    wx.navigateTo({
      url: './detail/detail?order=' + order
    })
  },
  onLoad: function (options) {
    // var t = JSON.parse(options.train);
    project_id=options.project_id;
    console.log(options)
    wx.request({
      url: app.globalData.server + 'student_api/get_group',
      method: "POST",
      data: {
        project_id: project_id,
        account: app.globalData.account,
      },
      success: res => {
        this.setData({
          messageList: res.result
        })
      },
    })
  }
})