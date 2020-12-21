// import http from '../services/http'
import request from '@/utils/request'

export function getPTAll() {
    return request({
        url: `/api/v1/pt/`,
        method: 'get',
    })
}



export function getPT(page=0,size,params) {
    return request({
        url: `/api/v1/pt/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function getPtObj(id) {
    return request({
        url: `/api/v1/pt/${id}`,
        method: 'get',
    })
}
