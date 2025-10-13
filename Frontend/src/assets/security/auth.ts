declare const __PASSWORD_HASH__: string | undefined

const TOKEN_KEY   = 'auth_token_v1'
const EXPIRES_KEY = 'auth_expires_v1'
const EXPECTED_HASH = (__PASSWORD_HASH__ ?? '').trim()

function toHex(buffer: ArrayBuffer) {
  return [...new Uint8Array(buffer)].map(b => b.toString(16).padStart(2, '0')).join('')
}

async function sha256Hex(text: string): Promise<string> {
  const { sha256 } = await import('js-sha256')
  return sha256(text)
}

// Constant-time comparison (frontend level, better than nothing)
function safeEqual(a: string, b: string) {
  if (a.length !== b.length) return false
  let out = 0
  for (let i = 0; i < a.length; i++) out |= a.charCodeAt(i) ^ b.charCodeAt(i)
  return out === 0
}

export function useAuth() {
  function isAuthed(): boolean {
    const token = localStorage.getItem(TOKEN_KEY) || ''
    const exp = Number(localStorage.getItem(EXPIRES_KEY) || 0)
    if (!EXPECTED_HASH || !token) return false
    // Critical fix: must verify token === EXPECTED_HASH
    return Date.now() < exp && safeEqual(token, EXPECTED_HASH)
  }

  async function login(password: string): Promise<boolean> {
    if (!EXPECTED_HASH) return false
    const hash = await sha256Hex(password)
    if (safeEqual(hash, EXPECTED_HASH)) {
      const exp = Date.now() + 24 * 60 * 60 * 1000 // 24h
      // Store expected hash itself, isAuthed uses it for equality verification
      localStorage.setItem(TOKEN_KEY, EXPECTED_HASH)
      localStorage.setItem(EXPIRES_KEY, String(exp))
      return true
    }
    logout()
    return false
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(EXPIRES_KEY)
  }

  return { isAuthed, login, logout }
}
