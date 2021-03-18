// pages/home/home.js
var app = getApp()

Page({
  data: {

    courseList: [{
      course_id: 0,
      course_name: "ooad",
      course_project: [{
        project_id: 7,
        project_name: "后端",
      }, {
        project_id: 6,
        project_name: "前端",
      }],
    }, {
      course_id: 1,
      course_name: "ai",
      course_project: [{
        project_id: 7,
        project_name: "ISE",
      }, {
        project_id: 6,
        project_name: "ISP",
      }],
    }]
  },
  onClick(e) {

    let project_id = e.target.id
    wx.request({
      url: app.globalData.server + 'wechart_api/check_group/',
      method: "POST",
      data: {
        account: app.globalData.account,
        project_id: project_id
      },
      success: res => {
        let group_info = res.data.group
        
        if (group_info) {
          wx.navigateTo({
            url: './groupmy/groupmy?group_id=' + group_info.group_id
          })
        } else {
          wx.navigateTo({
            url: './grouppage/grouppage?project_id=' + project_id
          })
        }

      },
    })

  },
  onShow() {

    wx.request({
      url: app.globalData.server + 'wechart_api/get_project/',
      method: "POST",
      data: {
        account: app.globalData.account
      },
      success: res => {
        console.log(res.data.course)
        this.setData({
          courseList: res.data.course
        })
      },
    })
  }
});