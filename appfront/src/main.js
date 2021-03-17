import Vue from 'vue'
import App from "./App.vue"
import router from "./router"
import axios from "axios"
import ElementUI from "element-ui"
import "element-ui/lib/theme-chalk/index.css"
import showdown from 'showdown'
import hljs from 'highlight.js/lib/highlight';
import 'highlight.js/styles/monokai-sublime.css';

var showdownHighlight = require("showdown-highlight")
Vue.prototype.md2html = (md)=> {
  let converter = new showdown.Converter(
    {
    extensions:[showdownHighlight]
  }
  )
  let text = md.toString()
  return converter.makeHtml(text)
}
Vue.use(ElementUI);
//全局配置
Vue.prototype.$axios = axios;
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  render: h => h(App)
})
