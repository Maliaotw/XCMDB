// import http from '../services/http'
import request from '@/utils/request'

export function getSettingsObj(name) {
    return request({
        url: `/api/v1/settings/${name}`,
        method: 'get',
    })
}



export function updateSettingsObj(name,data) {
    return request({
        url: `/api/v1/settings/${name}`,
        method: 'post',
        data
    })
}

export function getRolePermissions() {
    return request({
        url: '/api/v1/role-permission/',
        method: 'get'
    })
}

export function updateRolePermission(id, data) {
    return request({
        url: `/api/v1/role-permission/${id}/`,
        method: 'patch',
        data: data
    })
}
