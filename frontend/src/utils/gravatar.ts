import md5 from 'blueimp-md5'

import { GRAVATAR_BASE_URL } from '../config'

export function getGravatarUrl(email: string, size = 120) {
  return `${GRAVATAR_BASE_URL}/${md5(email.trim().toLowerCase())}?s=${size}&d=identicon`
}
