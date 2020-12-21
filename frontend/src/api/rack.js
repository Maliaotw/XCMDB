// import http from '../services/http'
import request from '@/utils/request'


export function getRackObj(id) {
    return request({
        url: `/api/v1/rack/${id}`,
        method: 'get',
    })
}

export function getRackDetailObj(id) {
    return request({
        url: `/api/v1/rack/detail/${id}`,
        method: 'get',
    })
}

export function getRackAll(params) {
    return request({
        url: `/api/v1/rack/`,
        method: 'get',
        params
    })
}



export function getRack(page=0,size,params) {
    return request({
        url: `/api/v1/rack/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function add(data) {
    return request({
        url: '/rack/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/rack/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/rack/' + id + '/',
        method: 'put',
        data
    })
}