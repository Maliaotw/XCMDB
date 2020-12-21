// import http from '../services/http'
import request from '@/utils/request'

export function getAsset(page,size,params) {
    return request({
        url: `/api/v1/assets/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function getAssetObj(id) {
    return request({
        url: `/api/v1/assets/${id}`,
        method: 'get',
    })
}


export function getStatus(page,size,params) {
    return request({
        url: `/api/v1/assets/status`,
        method: 'get',
        params
    })
}

export function getType(page,size,params) {
    return request({
        url: `/api/v1/assets/type`,
        method: 'get',
    })
}


export function add(data) {
    return request({
        url: '/api/v1/assets/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/assets/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/assets/' + id + '/',
        method: 'put',
        data
    })
}