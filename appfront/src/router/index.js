import Vue from "vue";
import Router from "vue-router";
import Login from "../components/Login";
import Register from "../components/Register";
import Information from "../components/information/Information";
import Find from "../components/Find";
import FindPassword from "../components/FindPassword";
import HomePage from "../components/HomePage";
import ProManage from "../components/ProManage";
import project from "../components/projectPage/project";
import groupMark from "../components/groupMarkPage/groupMark";
import HeadLine from "../components/HeadLine";


Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/login",
      name: "Login",
      component: Login
    },
    {
      path: "/register",
      name: "Register",
      component: Register
    },
    {
      path: "/mt",
      name: "MarkTemplate",
      component: () => import("../components/MarkTemplate/MarkTemplate")
    },
    {
      path: "/findpassword",
      name: "FindPassword",
      component: FindPassword
    },
    {
      path: "/404",
      component: () => import("../components/error/404"),
      name: "Page404"
    },
    {
      path: "/401",
      component: () => import("../components/error/401"),
      name: "Page401"
    },
    {
      path: "/:sid",
      name: "HomePage",
      component: HomePage,
      children: [
        {
          path: "header",
          component: HeadLine
        }
      ]
    },
    {
      path: "/teacher/:tid",
      name: "ProManage",
      component: ProManage
    },
    {
      path: "/team/:pid/find",
      name: "Find",
      component: Find
    },
    {
      path: "/:sid/information",
      name: "Information",
      component: Information,
    },
    {
      path: '*',
      redirect: '/404'
    },
    {
      path: "/groupMark/:gid",
      name: "group_mark",
      component: groupMark,
      props: (route) =>({ squery: route.query.qsid, tquery: route.query.qtid, saquery: route.query.qsaid})
    },
    {
      path: "/team/:gid",
      name: "student_project",
      component: project,
      props: (route) => ({ squery: route.query.qsid, tquery: route.query.qtid})
    },
  ],
  mode: "history"
});
