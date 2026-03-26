# Bhoomi AI — Study Notes
*Concepts covered up to Phase 1, Session ~6. Use these to revise before interviews.*

---

## 1. Hexagonal Architecture (Ports and Adapters)

### What problem does it solve?
In layered/MVC architecture, business logic gets tangled with database calls, HTTP details, and external APIs. A NASA API change forces you to touch your business logic. A database swap requires rewriting services. Hexagonal architecture inverts this: the domain is the centre, and everything else plugs into it.

### The layers

```
domain/          → Pure Python. Zero external imports. Business rules live here.
application/     → ports/ (Protocols) + services/. Orchestrates domain objects.
infrastructure/  → Adapters. Implements ports. Supabase, Redis, NASA, MQTT.
presentation/    → FastAPI routes. Under 15 lines. No business logic.
bootstrap.py     → The ONLY file that imports from both domain AND infrastructure.
```

### The key rule
The domain never imports from infrastructure. Ever. The architecture fitness test (`test_layer_imports.py`) scans `domain/` with `ast` and fails CI if any infrastructure import is found.

### Why only bootstrap.py wires things?
If services created their own adapters, you could not swap them for fakes in tests. `bootstrap.py` is the composition root — the single place where you say "use the real Supabase adapter in production." Tests use `InMemory` fakes instead.

### Interview question
*"Why hexagonal over MVC?"*
> In MVC, the model layer still tends to couple to the database. Hexagonal inverts the dependency: infrastructure depends on the domain, not the other way. If the NASA API changes, only `infrastructure/nasa/smap_adapter.py` changes. The domain is untouched.

---

## 2. Protocols (Python's version of interfaces)

### What they are
Python's `Protocol` (from `typing`) defines a structural interface — a contract that any class can satisfy without explicitly inheriting from it. This is called structural subtyping (or "duck typing with enforcement").

### Java analogy
`Protocol` in Python = `interface` in Java. `IMarketListingRepository` is the port. `SupabaseMarketListingRepository` and `InMemoryMarketListingRepository` are implementations.

### Why use them in ports?
The service depends on the Protocol, not the concrete class. This means:
- Unit tests inject `InMemoryMarketListingRepository` — no database needed
- Production wires `SupabaseMarketListingRepository` — real Supabase
- The service code does not change at all

### Example pattern
```
IMarketListingRepository (Protocol in application/ports/)
    ↑ implemented by
SupabaseMarketListingRepository (infrastructure/)   ← production
InMemoryMarketListingRepository (tests/fakes/)      ← unit tests
```

---

## 3. Domain Objects — Value Objects and Entities

### Value Object
Defined entirely by its values. Two value objects with the same values are equal. Immutable. No identity.
- Examples in this project: `Product`, `RegionalContext`, `PerishabilityLevel`
- In Python: `@dataclass(frozen=True)` makes it immutable

### Entity
Has a unique identity that persists over time. Two entities with the same data but different IDs are different.
- Examples: `MarketListing` (has `listing_id`), `ProducerProfile` (has `producer_id`)

### Why domain objects enforce their own invariants
The domain object is the last line of defence. It fires regardless of who calls it — a route, a background job, a test, a CLI. You cannot bypass it.

```python
# This raises InvalidPriceError no matter who calls it
MarketListing(..., listing_mode=ListingMode.SELL, price=Decimal('-5'), ...)
```

---

## 4. Enums in Python

Used to represent a fixed set of valid values. Unknown values raise an error — never silently default.

| Enum | Values |
|---|---|
| `ProducerType` | `FARMER, FISHERMAN, CATTLE_FARMER, POULTRY_FARMER` |
| `ProductCategory` | crop/livestock/fish categories |
| `ListingMode` | `SELL, DONATE, BOTH` |
| `PerishabilityLevel` | `CRITICAL (<6h), HIGH (1-3 days), MEDIUM (1 week), LOW (months)` |

### Key rule
If someone passes an invalid string, raise `InvalidProductCategoryError`. Never silently map it to a default.

---

## 5. ProducerProfile (Aggregate Root)

### What is an aggregate root?
The entry point for a cluster of related domain objects. All mutations go through it. You never reach inside and modify child objects directly.

### Key rules in this project
- `producer_types`: `frozenset[ProducerType]` — supports mixed farming (a producer can be `{FARMER, CATTLE_FARMER}`)
- Empty set → `NoProducerTypeError`
- Invalid value → `InvalidProducerTypeError`
- Every mutation checks ownership: if `requesting_producer_id != self.producer_id` → `UnauthorisedOperationError`
- Always go through `ProducerProfile` to modify products. Never reach inside directly.

---

## 6. MarketListing

### Business rules (enforced in domain)
- `price <= 0` for SELL mode → `InvalidPriceError`
- `listing_mode`: `SELL | DONATE | BOTH`
- `should_convert_to_donation(current_time)` — pure domain method, no I/O. Checks if a SELL listing should auto-convert to DONATE based on perishability window.

### PerishabilityLevel logic
| Level | Window | Example |
|---|---|---|
| CRITICAL | < 6 hours | Fresh fish |
| HIGH | 1–3 days | Dairy, leafy greens |
| MEDIUM | ~1 week | Root vegetables |
| LOW | Months | Grains, dried goods |

---

## 7. TDD — Test-Driven Development

### The cycle
**RED → GREEN → REFACTOR**
1. Write a failing test first. It must fail for the right reason.
2. Write the minimum code to make it pass.
3. Refactor without breaking the test.

### Why it's non-negotiable here
- Forces you to think about the interface before the implementation
- Catches regressions automatically
- Makes you write testable code (untestable code = bad design)

### Test categories in this project
| Category | What | When |
|---|---|---|
| `pytest` (default) | Unit tests, zero real I/O, under 10 seconds | Every change |
| `pytest -m integration` | Real Supabase | Manual before PRs |
| `pytest -m pi` | Raspberry Pi hardware | On Pi only |
| `pytest -m safety` | Physical safety invariants | Never skip, never mock |

### The fake rule
Unit tests use `InMemoryMarketListingRepository`, never real Supabase. Domain objects are pure Python — test them directly, never mock them.

---

## 8. Validation — Three Layers

Every piece of input passes through three guards:

```
Mobile App sends JSON
        ↓
Layer 1 — Pydantic schema (route boundary)
  • Is the shape correct?
  • Is listing_mode a valid enum value?
  • Is price a number, not a string?
  • Returns 422 if wrong — before any business logic runs
        ↓
Layer 2 — Service layer
  • Does this producer exist?
  • Are they allowed to do this action?
  • Requires database context — domain object can't do this
        ↓
Layer 3 — Domain object (innermost)
  • Are the business rules satisfied?
  • price <= 0 for SELL → InvalidPriceError
  • Fires no matter who called the service
```

**Why all three?** Each layer catches a different class of problem. A bug in Layer 1 could let malformed data reach Layer 2. If only Layer 1 validates, a service called from a background job has no protection.

---

## 9. JWT Authentication

### What is a JWT?
JSON Web Token. Three parts separated by dots: `header.payload.signature`

The **payload** contains claims — a JSON object:
```json
{
  "sub": "user_2abc123xyz",
  "email": "ravi@example.com",
  "role": "farmer",
  "iat": 1711234567,
  "exp": 1711238167
}
```

- `sub` = subject = the user's unique ID (Clerk user ID)
- `iat` = issued at (Unix timestamp)
- `exp` = expiry (Unix timestamp) — TTL is 1 hour in this project

### How it works end-to-end
1. Farmer logs in → Clerk issues a signed JWT
2. Mobile app stores it in `expo-secure-store` (never `AsyncStorage` — iOS Keychain / Android Keystore)
3. Every API call sends: `Authorization: Bearer <jwt>`
4. FastAPI middleware calls `verify_clerk_jwt()` — checks signature using Clerk's public key
5. If valid, middleware extracts `sub` → that is the `producer_id`
6. The route reads `producer_id` from the verified token — not from the request body

### Why producer_id must NOT be in the request body
If the body controls `producer_id`, any farmer can send someone else's `producer_id` and create a listing under their name. Identity must come from the verified token only — a JWT cannot be forged without Clerk's private key.

### Security headers required on every response
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Request-ID: <uuid per request>
```

---

## 10. Dependency Injection and bootstrap.py

### What is DI?
Instead of a class creating its own dependencies (`self.repo = SupabaseRepo()`), dependencies are passed in from outside (`def __init__(self, repo: IMarketListingRepository)`).

### Why it matters
- In tests: pass `InMemoryMarketListingRepository` — no database
- In production: pass `SupabaseMarketListingRepository` — real database
- The service code is identical in both cases

### The DI rule in this project
`bootstrap.py` is the only place that wires concrete adapters to services. No service creates its own adapter. No route creates its own service.

---

## 11. Mobile Security Rules (React Native / Expo)

| Rule | Wrong | Right |
|---|---|---|
| Token storage | `AsyncStorage` | `expo-secure-store` |
| Safe area padding | `paddingTop: 44` | `useSafeAreaInsets()` |
| API calls | In components | In custom hooks |
| Image upload | Raw camera photo | Strip EXIF first (removes GPS) |
| Deep link params | Use directly | Validate UUID before use |

---

## 12. Financial Integrity Rules

1. `NUMERIC(10,4)` for all price/cost/revenue columns — never `FLOAT` (floating point arithmetic is imprecise)
2. Append-only records — no UPDATE, no DELETE on financial data
3. Atomic transactions — escrow + commitment in a single transaction
4. `audit_log` table — all financial operations logged here, INSERT-only RLS

---

---

## 13. FastAPI — Routes, Routers, and Dependency Injection

### What FastAPI is
Python web framework — equivalent to Spring Boot in Java. You write a function, decorate it with a route path, FastAPI handles HTTP.

### How routes are organised

```
presentation/
    app.py           ← creates FastAPI app, mounts routers
    routes/
        health.py    ← GET /health
        market_listing.py  ← POST /listings
```

Each route file creates an `APIRouter`. `app.py` mounts all routers onto the main app with `app.include_router(...)`.

### Pydantic request schemas
The mobile app sends JSON. You define a Pydantic class — FastAPI parses and validates automatically. If a required field is missing or the wrong type, FastAPI returns 422 before your function runs. This is Layer 1 validation.

### Dependency Injection with `Depends()`
`Depends(some_function)` tells FastAPI: "call this function first, inject its return value into my route." This is how the route receives the service and the JWT claims — without creating them itself.

```python
@router.post("/listings")
def create_listing(
    request: CreateListingRequest,
    claims: dict = Depends(get_current_user),       # JWT injected
    service = Depends(get_market_listing_service)   # service injected
):
    producer_id = UUID(claims["sub"])
```

### The route's job — translation only
The route speaks HTTP. It receives strings and JSON. It converts them to typed Python objects (`UUID`, `Decimal`, enums) and passes them to the service. No business logic in the route.

---

## 14. `@contextmanager` and Transactions

The `with` statement in Python requires a context manager — something that sets up before the block and tears down after.

`@contextmanager` + `yield` makes any generator function work as a context manager:

```python
@contextmanager
def transaction(self):
    begin()
    try:
        yield          # ← code inside `with` block runs here
        commit()       # success path
    except:
        rollback()     # failure path
        raise          # re-raise so the caller knows
```

**Why it matters for transactions:** If `deactivate()` succeeds but `save()` raises, rollback undoes both. Either everything commits or nothing does — that is atomicity.

---

## 15. Python Module System

- Python treats each file as a module.
- When `uv run python backend/main.py` runs, Python adds `backend/` to `sys.path`.
- All imports resolve from `backend/` as the root: `from application.services.market_listing_service import ...`
- A class with no state and no shared methods is unnecessary in Python. Use a plain module-level function instead.
- `self` is only a parameter on class methods — plain functions have no `self`.

---

## 16. Human-in-the-Loop Architecture

### The core rule
> The AI advises. The farmer decides. For any action with financial, legal, physical, or reputational consequences, a human confirmation step is not optional — it is the architecture.

### The irreversibility test
Before automating anything, ask: is the consequence fully reversible?
- Sending a weather alert → reversible → no gate needed
- Opening an irrigation valve → not reversible → gate required
- Submitting an insurance claim → not reversible → biometric gate required

### The eight mandatory confirmation gates
| Action | Gate |
|---|---|
| Open irrigation valve | In-app tap |
| Submit insurance claim | Biometric + review |
| Submit rejection report | Biometric + review |
| Publish social content | Preview + explicit tap |
| Donate surplus produce | Final confirmation |
| Join pool with escrow | Review + explicit join |
| Delete account | Email + 30-day hold |
| Accept revenue split | Member vote |

### Human capacity vs human removal
The benchmark question: after using this feature for one season, does the farmer understand their farm better? Or do they just trust the app more? Features should build capacity, not dependency.

---

## Key Interview Questions You Should Be Able to Answer

1. **Why hexagonal over MVC?** Domain has zero external dependencies. Infrastructure changes don't touch business logic.
2. **What is structural subtyping?** A class satisfies a Protocol without inheriting from it — duck typing with enforcement.
3. **Why TDD?** Forces testable design. Regressions caught automatically. Interface-first thinking.
4. **What's in a JWT payload?** Claims — `sub` (user ID), `exp` (expiry), `iat` (issued at), role, email.
5. **Why not put producer_id in the request body?** Any client can forge it. Identity must come from the verified token.
6. **What is an aggregate root?** The entry point for a cluster of domain objects. All mutations go through it.
7. **Why three validation layers?** Each catches a different class of problem. No single layer can catch everything.
8. **Why frozenset for producer_types?** Immutable. Supports mixed farming. Equality comparison works correctly.
9. **What is bootstrap.py's job?** The composition root. The only file that touches both domain and infrastructure. Wires adapters to services.
10. **Why NUMERIC not FLOAT for money?** Float is IEEE 754 — `0.1 + 0.2 != 0.3`. Financial arithmetic must be exact.
11. **What does `Depends()` do in FastAPI?** Tells FastAPI to call a function before the route and inject its return value. Used for JWT auth and service injection.
12. **Why does the route convert `claims["sub"]` to UUID before calling the service?** The route speaks HTTP (strings). The service speaks domain (UUID). The route translates at the boundary. The service should never receive raw strings from HTTP.
13. **What is `@contextmanager` used for?** Makes a generator function work with `with`. Code before `yield` is setup, code after is teardown. Used for transactions: yield in try, commit on success, rollback on exception.
14. **Why did we make `build_services` a plain function instead of a class method?** The class had no state and one method. In Python, unnecessary classes add complexity without benefit. A module-level function is idiomatic.
15. **Where does the AI stop and the human start?** The AI advises, retrieves, translates, generates. The human confirms every action with financial, legal, physical, or reputational consequences.
