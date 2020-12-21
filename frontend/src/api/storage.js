// import http from '../services/http'
import request from '@/utils/request'

export function getStorageAll(page,size,params) {
    return request({
        url: `/api/v1/storage/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function getStorageObj(id) {
    return request({
        url: `/api/v1/storage/${id}`,
        method: 'get',
    })
}


export function del(id) {
    return request({
        url: '/api/v1/storage/' + id + '/',
        method: 'delete'
    })
}

