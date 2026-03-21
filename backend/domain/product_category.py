from enum import Enum, auto


class ProductCategory(Enum):
    # ── Classification failure ────────────────────────────────────────────────
    UNCLASSIFIED  = auto()   # agent failed to classify — triggers clarification prompt
                             # NEVER used in perishability or price feed routing
                             # logged as classification_failed in Langfuse

    # ── Grains & field crops ──────────────────────────────────────────────────
    GRAIN         = auto()   # wheat, rice, corn, barley, oats — MSP (IN) / CME (CA/US)
    PULSE         = auto()   # lentils, chickpeas, dal — AGMARKNET (IN) / local (CA)
    OILSEED       = auto()   # canola (CA), soybean (US), mustard (IN) — CME / AGMARKNET
    SUGARCANE     = auto()   # India FRP pricing — not MSP; different scheme mapping
    COTTON        = auto()   # India + USA; non-food — food safety rules do not apply
    FODDER        = auto()   # hay, silage, feed crops — LOW perishability; sold to cattle farmers

    # ── Horticulture ──────────────────────────────────────────────────────────
    VEGETABLE     = auto()   # tomatoes, onions, potatoes — HIGH perishability default
    FRUIT         = auto()   # mangoes, apples, berries — HIGH perishability default
    MUSHROOM      = auto()   # CRITICAL perishability (< 6h fresh); all three countries
    HERB          = auto()   # fresh herbs — distinct food-safety rules from vegetables
    SPICE         = auto()   # turmeric, chili, cardamom — India-primary; LOW perishability (dried)
    NUT           = auto()   # cashews (IN), almonds (US), hazelnuts (CA) — LOW perishability
    FLOWER        = auto()   # floriculture — non-food; food safety rules do not apply

    # ── Dairy — split because perishability varies too widely to collapse ─────
    MILK          = auto()   # raw/pasteurised milk — CRITICAL perishability (< 6h unrefrigerated)
    MILK_PRODUCTS = auto()   # paneer, yoghurt, buttermilk — HIGH perishability (1–3 days)
    CHEESE        = auto()   # aged = LOW (months); fresh mozzarella = HIGH — agent asks sub-type

    # ── Cattle ────────────────────────────────────────────────────────────────
    MEAT          = auto()   # beef, lamb, goat — CRITICAL/HIGH perishability; cold-chain required
    WOOL          = auto()   # sheep; non-perishable, non-food, no cold-chain, no food safety
    HIDE          = auto()   # cattle byproduct; non-perishable; marketplace listing only

    # ── Poultry ───────────────────────────────────────────────────────────────
    EGGS          = auto()   # MEDIUM perishability (1 week refrigerated)
    POULTRY       = auto()   # chicken, turkey, duck meat — HIGH perishability; cold-chain required

    # ── Seafood ───────────────────────────────────────────────────────────────
    FISH          = auto()   # finfish — Hilsa = CRITICAL, tilapia = HIGH; agent asks species
    SHRIMP        = auto()   # CRITICAL perishability; India + Canada both significant
    CRAB          = auto()   # CRITICAL perishability; live crab common in CA (BC) + IN (Kerala)
    LOBSTER       = auto()   # HIGH value — Nova Scotia (CA) + Kerala (IN); CRITICAL live
    SHELLFISH     = auto()   # mussels, oysters, clams — PEI (CA) + India coast; CRITICAL live
    SQUID         = auto()   # HIGH perishability; common India catch; moderate CA/US

    # ── Value-added — split on food safety axis, not on ingredient ───────────
    PRESERVED_FOOD = auto()  # jam, pickle, dried fish, fermented products
                             # canning / fermentation food safety rules apply (FDA/FSSAI/CFIA RAG)
    SHELF_STABLE   = auto()  # flour, rice bran, milled grain — no cold-chain, LOW perishability
                             # no food safety edge cases beyond standard storage
    CLARIFIED_FAT  = auto()  # ghee, lard, butter oil — LOW perishability; fat rancidity logic

    # ── Cross-producer ────────────────────────────────────────────────────────
    HONEY         = auto()   # beekeeping — LOW perishability; DONATE mode common; all three countries
    