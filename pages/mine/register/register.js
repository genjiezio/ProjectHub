// pages/mine/register/register.js
var app = getApp()

function countdown(that) {
  var second = that.data.second
  if (second == 0) {
    that.setData({
      label: "发送验证码",
      disabled: false
    });
    return;
  }
  var time = setTimeout(function () {
    that.setData({
      second: second - 1,
      label: (second - 1) + "s"
    });
    countdown(that);
  }, 1000)
}
Page({

  /**
   * 页面的初始数据
   */
  data: {
    "account": "",
    "password": "",
    "email": "",
    "code": "",
    "label": "发送验证码",
    "second": 60,
    "disabled": false
  },
  check(option) {
    if (!option.value) {
      wx.showToast({
        title: option.name + '不能为空',
        icon: 'none',
      })
      return false
    }
    return true
  },


  send: function (that) {
    if (this.data.email != "") {
      this.data.disabled = true;
      this.second = 60;
      countdown(this);
      wx.request({
        url: app.globalData.server + 'wechart_api/verify/', //获取服务器地址，此处为本地地址
        method: "POST",
        header: {
          "content-type": "application/x-www-form-urlencoded",
          'X-CSRFToken': app.globalData.csrf_token
        },
        data: { //向服务器发送的信息
          email: this.data.email
        },
        success: res => {
          if (res.data.status == 200) {
            app.globalData.account = this.data.account;
            app.globalData.get_userInfo = true;
          }
          wx.showToast({
            title: res.data.msg,
            icon: 'none',
            duration: 1500,
          })
        },
      })
    } else {
      wx.showToast({
        title: "请输入Email",
        icon: 'none',
        duration: 1500,
      })
    }

  },


  register: function () {
    let check_zreo = this.check({
      name: "账号",
      value: this.data.account
    }) && this.check({
      name: "密码",
      value: this.data.password
    }) && this.check({
      name: "邮箱",
      value: this.data.email
    }) && this.check({
      name: "验证码",
      value: this.data.code
    })
    if (!check_zreo) {
      return;
    }
    wx.request({
      url: app.globalData.server + 'wechart_api/create/', //获取服务器地址，此处为本地地址
      method: "POST",
      header: {
        "content-type": "application/x-www-form-urlencoded",
        'X-CSRFToken': app.globalData.csrf_token
      },
      data: {
        name: this.data.account,
        password: this.data.password,
        email: this.data.email,
        code: this.data.code
      },
      success: res => {
        if (res.data.status == 200) {
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
    // wx.cloud.callFunction({
    //   name: "postgres",
    //   data: {
    //     tp: 'i',
    //     fun: 0,
    //     account: this.data.account,
    //     password: this.data.password,
    //     role: this.data.role,
    //   }
    // }).then(
    //   res => {
    //     if (res.result == false) {
    //       wx.showToast({
    //         title: "账号已存在",
    //         icon: 'none',
    //       })
    //       return
    //     } else {
    //       wx.switchTab({
    //         url: '../mine'
    //       })
    //     }
    //   })

  },
  accountInput(e) {
    this.setData({
      account: e.detail,
    })
  },
  passwordInput(e) {
    this.setData({
      password: e.detail,
    })

  },
  emailInput(e) {
    this.setData({
      email: e.detail,
    })
  },
  codeInput(e) {
    this.setData({
      code: e.detail,
    })
  },

})