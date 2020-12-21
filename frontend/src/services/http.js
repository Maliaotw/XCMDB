import axios from 'axios'
import Cookies from 'js-cookie'
import store from '../store'
import app from '../main'
import VueCookie from "vue-cookie";


var master = axios.create({
    // baseURL: store.state.endpoints.baseUrl,
    baseURL: process.env.VUE_APP_BASE_API,
    // timeout: 15000,
    timeout: 600,
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken'),
        // Authorization: "Token " + store.state.token,
        // Authorization: "Token " + Cookies.get('csrftoken')
        Authorization: "Token " + store.state.users.token

    },
    xhrFields: {
        withCredentials: true
    }
})

master.interceptors.request.use(config => {
    app.$Progress.start()
    return config;
});

master.interceptors.response.use(
    response => {
        app.$Progress.finish()
        return response
    },
    error => {
        if (!error.response) {
            app.$Progress.fail()
            if (axios.isCancel(error)) {
                console.log("跳转取消")
                return Promise.reject(error)
            }
            if (error.message) {
                app.$message.error(error.message)
            } else {
                app.$message.error("unknow error")
            }
            return Promise.reject(error)
        }
        if (error.response.status === 401) {
            // 未輸入token 或 Token錯誤
            app.$Progress.fail()
            VueCookie.delete('csrftoken')
            VueCookie.delete('username')
            app.$router.push({name:'Login'})
            // this.$router.push({name: 'Login'})
            // window.location.reload()

            app.$notify.error({
                title: '错误',
                message: '未輸入token 或 Token錯誤123'
            });

            return Promise.reject(error)
        } else if (error.response.status >= 500) {
            app.$Progress.fail()
            app.$notify.error({
                title: '错误',
                message: '服务器出错啦 请联系管理员'
            });
            return Promise.reject(error)
        }

    })


export default master