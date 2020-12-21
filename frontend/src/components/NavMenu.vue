<template>
    <el-row class="tac">
        <el-col :span="24" class="h100">
            <el-menu
                    class="no-boarder el-menu-vertical-demo h100"
                    router
                    unique-opened
                    @open="handleOpen"
                    @close="handleClose"
                    background-color="#545c64"
                    text-color="#fff"
                    :default-active="activeTag"
                    ref="mySidemenu"
                    :collapse="!isNavMenuOpen"
                    active-text-color="#ffd04b"
                    mode="vertical"
            >

                <el-menu-item align="center">XCMDB</el-menu-item>

                <el-menu-item index="/Home">
                    <i class="el-icon-view"/>
                    <span>&nbsp;&nbsp;&nbsp;儀表盤</span>
                </el-menu-item>

                <el-submenu v-for="item in menu" :index="item.name" :key="item.name" class="no-boarder">
                    <template slot="title">
                        <i :class="item.meta.icon"/>&nbsp;
                        <span v-text="item.meta.title"/>
                    </template>
                    <el-menu-item-group class="over-hide" v-for="sub in item.sub" :key="sub.name">
                        <el-menu-item :index="sub.meta.index" v-text="sub.meta.title">
                        </el-menu-item>
                    </el-menu-item-group>
                </el-submenu>

                <el-menu-item index="/Home/Setting">
                    <i class="el-icon-setting"/>
                    <span>&nbsp;系統設置</span>
                </el-menu-item>

            </el-menu>
        </el-col>
    </el-row>
</template>

<style scoped>
    .h100 {
        height: 100%
    }

    .tac {
        position: fixed;
        top: 0px;
        bottom: 0px;
        z-index: 999;
    }

    .el-menu-vertical-demo:not(.el-menu--collapse) {
        width: 201px;
    }
</style>

<script>
    import {mapGetters, mapState} from 'vuex'
    import menu from '../config/menu-config'


    export default {
        data() {
            return {
                menu: menu,
                // activeTag:"",
                //  isNavMenuOpen: this.$store.state.users.isNavMenuOpen
                // isNavMenuOpen:""
            }
        },
        computed: {
          ...mapState(
                // ['users/isNavMenuOpen']
                {
                  isNavMenuOpen: state => state.users.isNavMenuOpen
                }
          ),

        },
        methods: {
            handleOpen(key, keyPath) {
                // 選單展開
                console.log(key, keyPath)
            },
            handleClose(key, keyPath) {
                // 選單
                console.log(key, keyPath)
            }
        },
        mounted () {
            console.log('mounted')
        },
        created() {
            // this.$store.commit('setActive', this.$route.path);
            // this.activeTag = this.$store.state.users.activeTag
          // this.$store.commit('users/setActive', this.$route.meta.index);
          this.activeTag = this.$route.meta.index


        }
    }
</script>
