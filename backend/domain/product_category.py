from enum import Enum, auto


class ProductCategory(Enum):
    # ── Crops ────────────────────────────────────────────────────────────────
    CROP        = auto()   # generic / uncategorised produce
    GRAIN       = auto()   # wheat, rice, corn, barley, oats — MSP/CME price feeds
    VEGETABLE   = auto()   # tomatoes, onions, potatoes — HIGH perishability default
    FRUIT       = auto()   # mangoes, apples, berries — HIGH perishability default
    PULSE       = auto()   # lentils, chickpeas, dal — India AGMARKNET + Canada
    OILSEED     = auto()   # canola (CA), soybean (US), mustard (IN) — CME/AGMARKNET
    SPICE       = auto()   # turmeric, chili, cardamom — India-specific
    HERB        = auto()   # fresh herbs; distinct food-safety rules from vegetables
    NUT         = auto()   # cashews, almonds, hazelnuts — LOW perishability
    MUSHROOM    = auto()   # CRITICAL perishability (< 6h fresh); all three countries
    FLOWER      = auto()   # floriculture; non-food — food safety rules do not apply
    COTTON      = auto()   # India + USA; non-food, no donation conversion
    SUGARCANE   = auto()   # India FRP pricing (not MSP); different scheme mapping
    FODDER      = auto()   # hay, silage — sold to cattle farmers; LOW perishability

    # ── Dairy & Cattle ───────────────────────────────────────────────────────
    DAIRY       = auto()   # milk, paneer, cheese — HIGH perishability
    MEAT        = auto()   # beef, lamb, goat — CRITICAL/HIGH perishability
    WOOL        = auto()   # sheep; non-perishable, non-food, no cold-chain
    HIDE        = auto()   # cattle byproduct; non-perishable, marketplace only

    # ── Poultry ──────────────────────────────────────────────────────────────
    EGGS        = auto()   # MEDIUM perishability (1 week refrigerated)
    POULTRY     = auto()   # chicken, turkey, duck meat — HIGH perishability

    # ── Seafood ──────────────────────────────────────────────────────────────
    FISH        = auto()   # finfish; Hilsa = CRITICAL, tilapia = HIGH
    SHRIMP      = auto()   # CRITICAL perishability; India + Canada both significant
    CRAB        = auto()   # CRITICAL perishability; live crab common in Canada/India
    LOBSTER     = auto()   # HIGH value; Nova Scotia (CA) and Kerala (IN)
    SHELLFISH   = auto()   # mussels, oysters, clams — PEI (CA) + India coast
    SQUID       = auto()   # HIGH perishability; India common catch

    # ── Value-added / Cross-producer ─────────────────────────────────────────
    HONEY       = auto()   # beekeeping; LOW perishability; DONATE mode common
    PROCESSED   = auto()   # ghee, jam, dried fish, flour — food safety rules differ
