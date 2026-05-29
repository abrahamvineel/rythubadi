type TokenPayload = {
    user_id: string
    name: string
    language: string
    province_state: string
    country: string
}

export function decodeToken(token: string): TokenPayload | null {
    try {
        const payload = token.split(".")[1]
        return JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")))
    } catch {
        return null
    }
}
