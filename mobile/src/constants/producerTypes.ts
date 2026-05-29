// Single source of truth for producer types across the app.
// To add a new type: add one entry here + one value in the backend ProducerType enum.
export const PRODUCER_TYPES = [
    { value: "FARMER",         label: "Farmer",         emoji: "🌾", defaultLocationName: "My Farm" },
    { value: "CATTLE_FARMER",  label: "Cattle Farmer",  emoji: "🐄", defaultLocationName: "My Cattle Station" },
    { value: "FISHERMAN",      label: "Fish Farmer",    emoji: "🐟", defaultLocationName: "My Fishpond" },
    { value: "POULTRY_FARMER", label: "Poultry Farmer", emoji: "🐔", defaultLocationName: "My Poultry Farm" },
] as const

export type ProducerTypeValue = typeof PRODUCER_TYPES[number]["value"]
