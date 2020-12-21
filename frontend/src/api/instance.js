// import http from '../services/http'
import request from '@/utils/request'

const url = 'instance';

export function getInstance(page,size,params) {
    return request({
        url: `/api/v1/${url}/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function get(name) {
    return request({
        url: `/api/v1/instancename/?hw_name=${name}`,
        method: 'get',
    })
}

export function add(data) {
    return request({
        url: `/api/v1/${url}/`,
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: `/api/v1/${url}/'${id}/`,
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: `/api/v1/${url}/'${id}/`,
        method: 'put',
        data
    })
}