// miniprogram/pages/home/log/log.js
var app = getApp()
Page({
  data: {
    typeName: 'password',
    account: "",
    password: ""
  },
  check(option) {
    // console.log(option)
    if (!option.value) {
      wx.showToast({
        title: option.name + '不能为空',
        icon: 'none',
      })
      return false
    }
    return true
  },
  log_user: function () {
    let check_zreo = this.check({
      name: "账号",
      value: this.data.account
    }) && this.check({
      name: "密码",
      value: this.data.password
    })
    if (!check_zreo) {
      return;
    }

    wx.request({
      url: app.globalData.server + 'wechart_api/login/', //获取服务器地址，此处为本地地址
      method: "POST",
      header: {
        "content-type": "application/x-www-form-urlencoded",
        'X-CSRFToken': app.globalData.csrf_token
      },
      data: { //向服务器发送的信息
        name: this.data.account,
        password: this.data.password,
      },
      success: res => {
        if (res.data.status == 200 || res.data.status == 207) {
          app.globalData.account = this.data.account;
          app.globalData.get_userInfo = true;
          wx.switchTab({
            url: '../mine'
          })
        }

        wx.showToast({
          title: res.data.msg,
          icon: 'none',
          duration: 1500,
        })
      },
    })
  },

  accountInput(e) {
    app.globalData.account = e.detail.value;
    this.setData({
      account: e.detail.value
    })
  },
  passwordInput(e) {
    this.setData({
      password: e.detail.value
    })
  },

})