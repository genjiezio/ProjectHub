// pages/message/message.js
var app = getApp()

Page({

  data: {
    messageList: [{
      project_name: "nn",
      project_class: "ss",
      project_message: "project_message"
    }, {
      project_name: "nd",
      project_class: "ds",
      project_message: "droject_message"
    }]
  },

  detail(e) {
    let order = JSON.stringify(this.data.orderData[e.currentTarget.id])
    wx.navigateTo({
      url: './detail/detail?order=' + order
    })
  },
  onShow() {
    wx.request({
      url: app.globalData.server + 'student_api/get_message',
      method: "GET",
      data: {},
      success: res => {
        this.setData({
          messageList: res.result
        })
      },
    })
  }
})