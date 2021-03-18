"use strict";
// const request = require('./request')
const server = 'http://127.0.0.1:8000'; //服务地址

const ERROR_CODE = {
  SUCCESS: 0, // 返回成功
  ERR_UNKOWN: -1, // 未知错误
  ERR_SYS_ERROR: -2, // 服务异常
  ERR_COMMON_BAD_PARAM: -11, // 参数错误
  ERR_COMMON_BAD_FORMAT: -12, // 格式错误
  ERR_COMMON_PERMISSION: -13, // 权限错误
  ERR_PAGE_SIZE_ERROR: -1001, // 页码大小超限
  ERR_WECHAT_LOGIN: 10001, // 需要登录
  ERR_MEETING_ROOM_TIMEOVER: 20001, // 时间已过
  ERR_MEETING_ROOM_INUSE: 20002 // 时间冲突
}

// 小程序登录
const api_login = function ({ account, password} = {}) {
  wx.request({
    server: server,
    path: '/student_api/wx_login',
    method: 'POST',
    data: {
      account: account,
      password: password,
    },
    header: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
}

module.exports = {
  ERROR_CODE: ERROR_CODE,
  api_login: api_login,
}
