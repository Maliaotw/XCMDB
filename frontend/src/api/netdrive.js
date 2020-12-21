// import http from '../services/http'
import request from '@/utils/request'

export function getNetDeviceAll(page,size,params) {
    return request({
        url: `/api/v1/netdevice/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function getNetDeviceDtail(id) {
    return request({
        url: '/api/v1/netdevice/' + id + '/',
        method: 'get',
    })
}


export function getType() {
    return request({
        url: '/api/v1/netdevice/type',
        method: 'get',
    })
}


export function add(data) {
    return request({
        url: '/api/v1/netdevice/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/netdevice/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/netdevice/' + id + '/',
        method: 'put',
        data
    })
}
