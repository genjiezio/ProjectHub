// pages/schedule/schedule.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    project_list:[],
    minDate: new Date().getTime(),
    maxDate: new Date(new Date().setMonth(new Date().getMonth() + 6, 1)- 1000 * 60 * 60 * 24).getTime(),
    formatter(day) {
      const month = day.date.getMonth() + 1;
      const date = day.date.getDate();

      if (month === 11) {
        if (date === 1) {
          day.topInfo = '劳动节';
        } else if (date === 4) {
          day.topInfo = '五四青年节';
        } else if (date === 11) {
          day.text = '今天';
        }
      }

      if (day.type === 'start') {
        day.bottomInfo = '入住';
      } else if (day.type === 'end') {
        day.bottomInfo = '离店';
      }

      return day;
    },
  },
  onShow() {
    wx.request({
      url: app.globalData.server + 'student_api/get_project',
      method: "GET",
      data: {},
      success: res => {
        this.setData({
          orderData: res.result
        })
      },
    })
  }

})