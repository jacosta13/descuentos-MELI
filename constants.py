#SECTION URL
URL_ALL_SITES = "https://api.mercadolibre.com/sites" 

URL_CAT_BY_SITE = "https://api.mercadolibre.com/sites/{site}/categories/all"

URL_ITEMS_DISC = "https://api.mercadolibre.com/sites/{site}/search?category={category}&offset={offset}&sort=relevance&discount=5-100"

URL_SITE_CAT_OFFSET_DISC = """
https://api.mercadolibre.com/sites/{site}/search?category={category}&offset={offset}&sort=relevance&limit=50&discount=5-100
"""

URL_SITE_CAT_OFFSET = """
https://api.mercadolibre.com/sites/{site}/search?category={category}&offset={offset}&sort=relevance&limit=50
"""

# SECTION KEYS

KEYS_DIRECT_VALUES = [
    'id', 
    'site_id',
    'title', 
    'price', 
    'sale_price', 
    'currency_id',
    'available_quantity',
    'sold_quantity',
    'buying_mode',
    'listing_type_id',
    'stop_time', 
    'condition', 
    'permalink',
    'thumbnail', 
    'thumbnail_id', 
    'accepts_mercadopago',
    'original_price',
    'category_id', 
    'official_store_id', 
    'domain_id',
    'catalog_product_id', 
    'order_backend', 
    'use_thumbnail_id',
    'offer_score',
    'offer_share', 
    'match_score', 
    'winner_item_id',
    'melicoin'
]

KEYS_COMPLEX_VALUES = [
    'seller',
    'prices',
    'installments',
    'address',
    'shipping',
    'seller_address',
    'attributes',
    'tags'
]

KEYS_SELLER = [
    'id', 
    'permalink',
    'registration_date', 
    'car_dealer', 
    'real_estate_agency', 
    'tags'
]

KEYS_JSON_TYPES = {
    "seller":[
        "id",
        "permalink",
        "registration_date",
        "car_dealer",
        "real_estate_agency",
        "tags",
    ],
    "prices":[
        "id",
        "prices",
        "presentation",
        "payment_method_prices",
        "reference_prices",
        "purchase_discounts",
    ],
    "installments":[
        "quantity",
        "amount",
        "rate",
        "currency_id",
    ],
    "address":[
        "state_id",
        "state_name",
        "city_id",
        "city_name",
    ],
    "shipping":[
        "free_shipping",
        "mode",
        "tags",
        "logistic_type",
        "store_pick_up",
    ],
    "seller_address":[
        "id",
        "comment",
        "address_line",
        "zip_code",
        "country.name",
        "state.name",
        "city.name",
        "latitude",
        "longitude",
    ]
}

KEYS_LIST_TYPES = [
    "attributes",
    "tags"
]

ATTRIBUTES_IDS = [
    "ITEM_CONDITION",
    "BRAND",
    "MODEL"
]

TAGS = [
    "best_seller_candidate",
    "loyalty_discount_eligible",
    "good_quality_picture"
]