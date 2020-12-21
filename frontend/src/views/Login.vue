<template>
    <el-container>
        <el-header></el-header>
        <el-main class="main">
            <h1>後台</h1>
            <el-form ref="form" :model="form" class="z-depth-2">
                <el-form-item>
                    <el-input v-model="form.username" placeholder="email"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-input v-model="form.password" placeholder="password" type="password"></el-input>
                </el-form-item>
                <el-form-item style="text-align:right;">
                    <el-button type="primary" @click="login">登录</el-button>
                </el-form-item>
            </el-form>
        </el-main>
        <el-footer></el-footer>
    </el-container>
</template>

<script>
    import VueCookie from 'vue-cookie'
    import {mapState} from "vuex";

    export default {
        name: 'Login',
        data() {
            return {
                form: {
                    username: 'admin',
                    password: ''
                }
            }
        },
        methods: {
            reloadPage() {
                window.location.reload()
            },
            login() {
                const payload = {
                    username: this.form.username,
                    password: this.form.password
                }
                // console.log(payload)
                self = this
                this.$axios.post("/api/v1/api-token-auth/", payload)
                    .then((result) => {
                        console.log(result.data)
                        VueCookie.set('csrftoken', result.data.token, 14)
                        VueCookie.set('username', result.data.username, 14)
                        self.reloadPage()
                    })
            }
        },
        created() {
        //     if (this.$store.state.users.token) {
            if (this.token !== "") {
                // TODO 要在驗證一下
                // console.log(this.$store.state)
                this.$router.push({name: 'Home'})
            }
        },
        // watch:{
        //   token: function(val){
        //     console.log(val)
        //     this.$router.push({name: 'Home'})
        //     this.reloadPage()
        //   }
        // },
        computed: {
            // ...mapGetters(['isNavMenuOpen']),
            ...mapState(
                // ['users/isNavMenuOpen']
                {
                  token: state => state.users.token
                }
            ),
        }

    }
</script>

<style scoped>
    h1 {
        text-align: center;
        color: #606266;
    }

    form {
        padding: 20px;
        background: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
        border-radius: 2px;
    }

    .main {
        width: 400px;
        margin: 0px auto;
    }
</style>
