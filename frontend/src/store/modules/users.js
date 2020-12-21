import {logout, getProfile} from '@/api/users'
import {
    getTokenFromCookie,
    getCurrentOrgFromCookie,
    saveCurrentOrgToCookie,
    getCurrentRoleFromCookie,
    saveCurrentRoleToCookie,
    getUsernameCookie
} from '@/utils/auth'
import {resetRouter} from '@/router'
import rolec from '@/utils/role'

const getDefaultState = () => {
    return {
        token: getTokenFromCookie(),
        username: getUsernameCookie(),
        currentOrg: getCurrentOrgFromCookie(),
        currentRole: getCurrentRoleFromCookie(),
        profile: {},
        roles: {},
        orgs: [],
        perms: 0b00000000,
        MFAVerifyAt: null,
        navTags: [],
        isNavMenuOpen: true,
        isAuthenticated: false,
        active: "",
    }
}

const state = getDefaultState()

const mutations = {
    RESET_STATE: (state) => {
        Object.assign(state, getDefaultState())
    },
    SET_TOKEN: (state, token) => {
        state.token = token
    },
    SET_PROFILE: (state, profile) => {
        state.profile = profile
    },
    SET_ORGS: (state, orgs) => {
        state.orgs = orgs
    },
    ADD_ORG: (state, org) => {
        state.orgs.push(org)
    },
    SET_ROLES(state, roles) {
        state.roles = roles
    },
    SET_PERMS(state, perms) {
        state.perms = perms
    },
    SET_CURRENT_ORG(state, org) {
        saveCurrentOrgToCookie(org)
        state.currentOrg = org
    },
    SET_CURRENT_ROLE(state, role) {
        saveCurrentRoleToCookie(role)
        state.currentRole = role
    },
    SET_MFA_VERIFY(state) {
        state.MFAVerifyAt = (new Date()).valueOf()
    },

    toggleMenuOpen(state, payload) {
        state.isNavMenuOpen = !state.isNavMenuOpen
    },

}

const actions = {

    // get user Profile
    getProfile({commit, state}, refresh = false) {
        return new Promise((resolve, reject) => {
            if (!refresh && state.profile && Object.keys(state.profile).length > 0) {
                resolve(state.profile)
                return
            }
            getProfile().then(response => {
                if (!response) {
                    reject('Verification failed, please Login again.')
                }
                commit('SET_PROFILE', response)
                resolve(response)
            }).catch(error => {
                console.log(error)
                reject(error)
            })
        })
    },
    getRoles({commit, dispatch, state}, refresh) {
        return new Promise((resolve, reject) => {
            if (!refresh && state.roles && state.roles.length > 0) {
                return resolve(state.roles)
            }
            return dispatch('getProfile').then((profile) => {
                const {current_org_roles: currentOrgRoles, role} = profile
                const roles = rolec.parseUserRoles(currentOrgRoles, role)
                commit('SET_ROLES', roles)
                commit('SET_PERMS', rolec.sumPerms(roles))
                resolve(roles)
            }).catch((e) => {
                reject(e)
            })
        })
    },
    getInOrgs({commit, dispatch, state}, refresh) {
        return new Promise((resolve, reject) => {
            if (!refresh && state.role && state.role.length > 0) {
                return resolve(state.roles)
            }
            dispatch('getProfile').then(profile => {
                const {admin_or_audit_orgs: inOrgs} = profile
                commit('SET_ORGS', inOrgs)
                resolve(inOrgs)
            }).catch((e) => reject(e))
        })
    },
    addAdminOrg({commit, state}, org) {
        commit('ADD_ORG', org)
    },



    removeOneNavTag(state, payload) {
        let index = state.navTags.findIndex((item) => {
            return item.index === payload.index
        })
        if (index === -1) {
            return
        }
        state.navTags.splice(index, 1)
    },

    updateToken(state, {newToken,}) {
        // TODO: For security purposes, take localStorage out of the project.
        localStorage.setItem('token', newToken);
        state.jwt = newToken;
        Cookies.set('token', newToken)

        // Vue.set(state, 'jwt', newToken)
    },
    removeToken(state) {
        // TODO: For security purposes, take localStorage out of the project.
        state.jwt = "";
        state.authUser = "";
        localStorage.removeItem('token');
        localStorage.removeItem('authUser');
        localStorage.removeItem('isAuthenticated');
        // state.jwt = null;

    },

    // user logout
    logout({commit, state}) {
        return new Promise((resolve, reject) => {
            logout(state.token).then(() => {
                // removeToken() // must remove  token  first
                resetRouter()
                commit('RESET_STATE')
                resolve()
            }).catch(error => {
                reject(error)
            })
        })
    },
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}
