import Cookies from 'js-cookie'

const TOKEN_KEY = 'x_auth_token'
const ACCESS_TOKEN_KEY = 'x_access_token'
const REFRESH_TOKEN_KEY = 'x_refresh_token'
const ROLES_KEY = 'x_user_roles'
const CURRENT_ORG_KEY = 'jms_current_org'
const CURRENT_ROLE_KEY = 'jms_current_role'
const USERNAME_KEY = 'username'

export function getAccessToken() {
  return Cookies.get(ACCESS_TOKEN_KEY)
}

export function setAccessToken(token) {
  return Cookies.set(ACCESS_TOKEN_KEY, token, { expires: 14 })
}

export function getRefreshToken() {
  return Cookies.get(REFRESH_TOKEN_KEY)
}

export function setRefreshToken(token) {
  return Cookies.set(REFRESH_TOKEN_KEY, token, { expires: 14 })
}

export function getUserRoles() {
  const roles = Cookies.get(ROLES_KEY)
  try {
    return roles ? JSON.parse(roles) : []
  } catch (e) {
    return []
  }
}

export function setUserRoles(roles) {
  return Cookies.set(ROLES_KEY, JSON.stringify(roles), { expires: 14 })
}

export function getTokenFromCookie() {
  return Cookies.get(TOKEN_KEY)
}

export function getUsernameCookie() {
  return Cookies.get(USERNAME_KEY)
}

export function getCurrentRoleFromCookie() {
  const role = Cookies.get(CURRENT_ROLE_KEY)
  if (role) {
    return parseInt(role) || null
  }
  return role
}

export function saveCurrentRoleToCookie(role) {
  console.log('Save current role to cookie: ', role)
  return Cookies.set(CURRENT_ROLE_KEY, role, { expires: 14 })
}

export function getCurrentOrgFromCookie() {
  let org = null
  try {
    org = JSON.parse(Cookies.get(CURRENT_ORG_KEY))
  } catch (e) {
    console.log('Current org in cookie: ', org)
  }
  return org
}

export function saveCurrentOrgToCookie(org) {
  Cookies.set(CURRENT_ORG_KEY, JSON.stringify(org), { expires: 14 })
  Cookies.set('X-JMS-ORG', org.id, { expires: 14 })
}

export function removeCurrentOrg() {
  return Cookies.remove(CURRENT_ORG_KEY)
}

export function removeAuthCookies() {
  Cookies.remove(TOKEN_KEY)
  Cookies.remove(ACCESS_TOKEN_KEY)
  Cookies.remove(REFRESH_TOKEN_KEY)
  Cookies.remove(ROLES_KEY)
  Cookies.remove(USERNAME_KEY)
  Cookies.remove(CURRENT_ORG_KEY)
  Cookies.remove(CURRENT_ROLE_KEY)
}
