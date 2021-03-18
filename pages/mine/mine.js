// pages/mine/mine.js
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  getUserInfo: function () {
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          wx.getUserInfo({
            success: res => {
              app.globalData.userInfo = res.userInfo;
              app.globalData.show = true;
              this.setData({
                userInfo: res.userInfo,
              })
            }
          })
        }
      }
    })
  },
  onShow() {
    var that = this
    var get_userInfo = app.globalData.get_userInfo;

    var account = app.globalData.account;

    if (get_userInfo) {
      this.getUserInfo()
    }

    that.setData({
      account: account,
      show: get_userInfo,
    });
  },
})