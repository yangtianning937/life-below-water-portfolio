// src/security/auth.ts
const TOKEN_KEY = 'auth_token_v1'
const EXPIRES_KEY = 'auth_expires_v1'

const EXPECTED_HASH = (__PASSWORD_HASH__ || '').trim()

function toHex(buffer: ArrayBuffer) {
  return [...new Uint8Array(buffer)].map(b => b.toString(16).padStart(2,'0')).join('')
}

async function sha256Hex(text: string) {
  const enc = new TextEncoder().encode(text)
  const buf = await crypto.subtle.digest('SHA-256', enc)
  return toHex(buf)
}

// 常量时间比较（前端聊胜于无）
function safeEqual(a: string, b: string) {
  if (a.length !== b.length) return false
  let out = 0
  for (let i = 0; i < a.length; i++) out |= a.charCodeAt(i) ^ b.charCodeAt(i)
  return out === 0
}

export function useAuth() {
  function isAuthed(): boolean {
    const token = localStorage.getItem(TOKEN_KEY)
    const exp = Number(localStorage.getItem(EXPIRES_KEY) || 0)
    return Boolean(token) && Date.now() < exp
  }

  async function login(password: string): Promise<boolean> {
    const hash = await sha256Hex(password)
    if (EXPECTED_HASH && safeEqual(hash, EXPECTED_HASH)) {
      const exp = Date.now() + 24 * 60 * 60 * 1000 // 24小时
      localStorage.setItem(TOKEN_KEY, hash)
      localStorage.setItem(EXPIRES_KEY, String(exp))
      return true
    }
    return false
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(EXPIRES_KEY)
  }

  return { isAuthed, login, logout }
}
