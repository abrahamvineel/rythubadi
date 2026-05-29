// To add a new country: add one entry to COUNTRIES. Nothing else changes.
export type Country = { code: string; name: string; flag: string }

export const COUNTRIES: Country[] = [
    { code: "CA", name: "Canada",        flag: "🇨🇦" },
    { code: "US", name: "United States", flag: "🇺🇸" },
    { code: "IN", name: "India",         flag: "🇮🇳" },
]
