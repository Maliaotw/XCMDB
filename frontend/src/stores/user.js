import { defineStore } from 'pinia'
import axios from 'axios'
import { logout, getProfile } from '@/api/users'
import Cookies from 'js-cookie'
import {
  getTokenFromCookie,
  getCurrentOrgFromCookie,
  saveCurrentOrgToCookie,
  getCurrentRoleFromCookie,
  saveCurrentRoleToCookie,
  getUsernameCookie,
  removeAuthCookies
} from '@/utils/auth'
import { resetRouter } from '@/router'
import rolec from '@/utils/role'

export const useUserStore = defineStore('user', {
  state: () => ({
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
    active: '',
    isSystemAdminView: false
  }),

  getters: {
    token: (state) => state.token,
    username: (state) => state.username,
    activeTag: (state) => state.active,
    isAuthenticated: (state) => state.isAuthenticated
  },

  actions: {
    resetState() {
      removeAuthCookies()
      const defaultState = {
        token: '',
        username: '',
        currentOrg: null,
        currentRole: null,
        profile: {},
        roles: {},
        orgs: [],
        perms: 0b00000000,
        MFAVerifyAt: null,
        navTags: [],
        isNavMenuOpen: true,
        isAuthenticated: false,
        active: '',
        isSystemAdminView: false
      }
      Object.assign(this, defaultState)
    },
    setToken(token) {
      this.token = token
    },
    setProfile(profile) {
      this.profile = profile
    },
    setOrgs(orgs) {
      this.orgs = orgs
    },
    addOrg(org) {
      this.orgs.push(org)
    },
    setRoles(roles) {
      this.roles = roles
    },
    setPerms(perms) {
      this.perms = perms
    },
    setCurrentOrg(org) {
      saveCurrentOrgToCookie(org)
      this.currentOrg = org
    },
    setCurrentRole(role) {
      saveCurrentRoleToCookie(role)
      this.currentRole = role
    },
    setMFAVerify() {
      this.MFAVerifyAt = Date.now()
    },
    toggleMenuOpen() {
      this.isNavMenuOpen = !this.isNavMenuOpen
    },
    setAdminView(val) {
      this.isSystemAdminView = val
    },
    removeOneNavTag(payload) {
      const index = this.navTags.findIndex((item) => item.index === payload.index)
      if (index !== -1) {
        this.navTags.splice(index, 1)
      }
    },
    async getProfile(refresh = false) {
      return new Promise((resolve, reject) => {
        if (!refresh && this.profile && Object.keys(this.profile).length > 0) {
          resolve(this.profile)
          return
        }
        getProfile()
          .then((response) => {
            if (!response) {
              reject('Verification failed, please Login again.')
            }
            this.setProfile(response)
            resolve(response)
          })
          .catch((error) => {
            console.log(error)
            reject(error)
          })
      })
    },
    async getRoles(refresh) {
      return new Promise((resolve, reject) => {
        if (!refresh && this.roles && this.roles.length > 0) {
          return resolve(this.roles)
        }
        return this.getProfile().then((profile) => {
          const { current_org_roles: currentOrgRoles, role } = profile
          const roles = rolec.parseUserRoles(currentOrgRoles, role)
          this.setRoles(roles)
          this.setPerms(rolec.sumPerms(roles))
          resolve(roles)
        }).catch((e) => {
          reject(e)
        })
      })
    },
    async getInOrgs(refresh) {
      return new Promise((resolve, reject) => {
        if (!refresh && this.role && this.role.length > 0) {
          return resolve(this.roles)
        }
        this.getProfile().then((profile) => {
          const { admin_or_audit_orgs: inOrgs } = profile
          this.setOrgs(inOrgs)
          resolve(inOrgs)
        }).catch((e) => reject(e))
      })
    },
    addAdminOrg(org) {
      this.addOrg(org)
    },
    async login(payload) {
      return axios.post('/api/v1/api-token-auth/', payload)
        .then((response) => {
          const { token, access_token, refresh_token, username, roles, menus, actions } = response.data

          // Set cookies using js-cookie (matching old vue-cookie behavior)
          Cookies.set('x_auth_token', token, { expires: 14 })
          Cookies.set('x_access_token', access_token, { expires: 14 })
          Cookies.set('x_refresh_token', refresh_token, { expires: 14 })
          Cookies.set('x_user_roles', JSON.stringify(roles), { expires: 14 })
          Cookies.set('username', username, { expires: 14 })
          Cookies.set('x_user_menus', JSON.stringify(menus), { expires: 14 })
          Cookies.set('x_user_actions', JSON.stringify(actions), { expires: 14 })

          // Update store state
          this.setToken(token)
          this.username = username
          this.isAuthenticated = true

          return response.data
        })
    },
    async logout() {
      return new Promise((resolve, reject) => {
        logout(this.token)
          .then(() => {
            resetRouter()
            this.resetState()
            resolve()
          })
          .catch((error) => {
            reject(error)
          })
      })
    }
  }
})
