// import http from '../services/http'
import request from '@/utils/request'

export function getNetworkAll() {
    return request({
        url: `/api/v1/network/`,
        method: 'get',
    })
}



export function AddNetwork(name = "network", data) {
    return request({
        url: `/api/v1/${name}/`,
        method: 'post',
        data
    })
}

export function DelNetwork(id) {
    return request({
        url: `/api/v1/network/${id}/`,
        method: 'delete',
    })
}

export function EditNetwork(id, data) {
    return request({
        url: `/api/v1/network/${id}/`,
        method: 'put',
        data
    })
}


export function getNetworkObj(id) {
    return request({
        url: `/api/v1/network/${id}`,
        method: 'get',
    })
}

export function getNetStatic( page = 0, size, params) {
    return request({
        url: `/api/v1/netstatic/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function PutNetStatic( id,data) {
    return request({
        url: `/api/v1/netstatic/${id}/`,
        method: 'put',
        data
    })
}

export function AddNetStatic(data) {
    return request({
        url: `/api/v1/netstatic/`,
        method: 'post',
        data
    })
}

export function DelNetStatic(id) {
    return request({
        url: `/api/v1/netstatic/${id}/`,
        method: 'delete',
    })
}


export function getNetwork( page = 0, size, params) {
    return request({
        url: `/api/v1/network/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function getHost(page = 0, size, params) {
    return request({
        url: `/api/v1/host/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function getHostAll() {
    return request({
        url: `/api/v1/host`,
        method: 'get',
    })
}

export function getHostobj(id) {
    return request({
        url: `/api/v1/host/${id}`,
        method: 'get',
    })
}




export function putDataStoreobj(id,data) {
    return request({
        url: `/api/v1/datastore/${id}/`,
        method: 'put',
        data
    })
}

export function putNetworkobj(id,data) {
    return request({
        url: `/api/v1/network/${id}/`,
        method: 'put',
        data
    })
}

export function getDatastore(page = 0, size, params) {
    return request({
        url: `/api/v1/datastore/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}


export function getClusterAll() {
    return request({
        url: `/api/v1/cluster`,
        method: 'get',
    })
}



export function getCluster(page = 0, size, params) {
    return request({
        url: `/api/v1/cluster/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function getClusterobj(id) {
    return request({
        url: `/api/v1/cluster/${id}`,
        method: 'get',
    })
}



export function putClusterobj(id,data) {
    return request({
        url: `/api/v1/cluster/${id}/`,
        method: 'put',
        data
    })
}

