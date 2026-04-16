CREATE TYPE listing_mode AS ENUM ('SELL', 'DONATE', 'BOTH');
CREATE TYPE product_category AS ENUM 
('UNCLASSIFIED', 'GRAIN', 'PULSE', 'OILSEED', 'SUGARCANE', 
'COTTON', 'FODDER', 'VEGETABLE', 'FRUIT', 'MUSHROOM', 'HERB', 
'SPICE', 'NUT', 'FLOWER', 'MILK', 'MILK_PRODUCTS', 'CHEESE', 
'MEAT', 'WOOL', 'HIDE', 'EGGS', 'POULTRY', 'FISH', 'SHRIMP', 
'CRAB', 'LOBSTER', 'SHELLFISH', 'SQUID', 'PRESERVED_FOOD', 
'SHELF_STABLE','CLARIFIED_FAT', 'HONEY');
CREATE TYPE perishability_level AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW');

CREATE TABLE IF NOT EXISTS market_listing (
    listing_id UUID PRIMARY KEY,
    listing_mode listing_mode NOT NULL,
    price NUMERIC(10, 4) NOT NULL,
    product_category product_category NOT NULL,
    perishability_level perishability_level NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    producer_id UUID NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    photo_url VARCHAR(2048)
);
