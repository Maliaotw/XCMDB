export default [

    {
        name: 'base',
        meta: {
            title: '基礎資源',
            icon: 'el-icon-box'
        },
        sub: [
            {
                name: 'Asset',
                meta: {
                    index: `/Home/Asset`,
                    title: '資產列表',
                    type: 'menu',
                    active: false
                },
                // component: import('../views/Basic/Asset.vue')
                component: () => import('../views/Basic/Asset.vue')
            },
            {

                name: 'Idrac',
                meta: {
                    index: `/Home/Idrac`,
                    title: '物理服務器',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/Basic/Idrac.vue')
            },
            {
                name: 'NetDevice',
                meta: {
                    index: `/Home/NetDevice`,
                    title: '網路設備',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/Basic/NetDevice.vue')
            },

            {
                name: 'Tag',
                meta: {
                    index: `/Home/Tag`,
                    title: '標籤列表',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/Basic/Tag.vue')
            }
        ]
    },
    {
        name: 'manager',
        meta: {
            title: '業務資源',
            icon: 'el-icon-bank-card'
        },
        sub: [
            {
                name: 'Host',
                meta: {
                    index: `/Home/Host`,
                    title: '虛擬機',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/Bus/Host.vue')
            },

        ]
    },
    {
        name: 'VMWare',
        meta: {
            title: 'VMware',
            icon: 'el-icon-copy-document'
        },
        sub: [
            {
                name: 'Cluster',
                meta: {
                    index: `/Home/Cluster`,
                    title: 'Cluster',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/VM/Cluster')
            },
            {
                name: 'PHost',
                meta: {
                    index: `/Home/PHost`,
                    title: 'ESXI',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/VM/PHost')
            },
            {
                name: 'Instance',
                meta: {
                    index: `/Home/Instance`,
                    title: 'Instance',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/VM/Instance')
            },

        ]
    }
    ,
    {
        name: '機房管理',
        meta: {
            title: '機房管理',
            icon: 'el-icon-mobile'
        },
        sub: [
            {
                name: 'IDC',
                meta: {
                    index: `/Home/IDC`,
                    title: '機房列表',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/Idc/idc')
            },
            {
                name: 'Rack',
                meta: {
                    index: `/Home/Rack`,
                    title: '機櫃列表',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/Idc/rack')
            },
            {
                name: 'ISP',
                meta: {
                    index: `/Home/ISP`,
                    title: 'ISP資訊',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/Idc/isp')
            }
        ]
    },
    {
        name: '作業中心',
        meta: {
            title: '作業中心',
            icon: 'el-icon-date'
        },
        sub: [
            {
                name: 'pt',
                meta: {
                    index: `/Home/pt`,
                    title: '任務列表',
                    type: 'menu',
                    active: false
                },
                component: () => import('../views/Task/pt')
            },
        ]
    },
    {
        name: '日誌審計',
        meta: {
            title: '日誌審計',
            icon: 'el-icon-menu'
        },
        sub: [{
            name: '登入歷史',
            meta: {
                index: `/Home/LoginLog`,
                title: '登入歷史',
                type: 'menu',
                active: false
            },
            component: () => import('../views/Audit/loginlog.vue')
        }]
    }


]
