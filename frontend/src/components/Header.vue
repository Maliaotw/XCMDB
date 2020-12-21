<template>
    <el-row>

        <el-col :span="2" class="header-wrap">
            <!-- 折疊menu  -->
            <el-button class="no-b" :icon="iconName" @click="toggleMenuOpen"/>
        </el-col>

        <el-col :span="2" class="header-wrap text-r" style="float: right;margin-right: 5px">
            <el-dropdown>
                <el-button class="no-b">
                    {{username}} <i class="fa fa-user-circle" aria-hidden="true"/> <i
                        class="el-icon-arrow-down el-icon--right"/>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item>
                        <i class="fa fa-address-card-o"/>
                        查看个人信息
                    </el-dropdown-item>
                    <el-dropdown-item @click.native="logout">
                        <i class="fa fa-power-off"/>
                        登出
                    </el-dropdown-item>
                    <el-dropdown-item>
                        <i class="fa fa-wrench"/>
                        修改密码
                    </el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </el-col>
    </el-row>
</template>

<script>
    import {mapGetters, mapState} from 'vuex'
    import VueCookie from 'vue-cookie'

    export default {
        data() {
            return {
                username: this.$store.state.users.username,
            };
        },
        methods: {
            logout() {
                VueCookie.delete('csrftoken')
                VueCookie.delete('username')
                // this.$router.push({name: 'Login'})
                window.location.href = '/'
                window.location.reload()
            },
            toggleMenuOpen() {
                this.$store.commit('users/toggleMenuOpen')
            }
        },
        computed: {
            // ...mapGetters(['isNavMenuOpen']),
            ...mapState(
                {
                  isNavMenuOpen: state => state.users.isNavMenuOpen
                }
            ),
            iconName() {
                return this.isNavMenuOpen ? 'fa fa-outdent' : 'fa fa-indent'
            }
        }
    }
</script>


<style scoped>
    .no-b {
        border: none !important
    }

    .text-r {
        text-align: right
    }

    .head-wrap {
        height: 40px;
        border-bottom: 1px solid #eee;
    }
</style>
