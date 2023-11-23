# API Specification


# 1. Accounts

## 1.1 Create Account - `/users/create` (POST)
Users create an account

**Request**:

```json
{
    "username": "string",
    "password": "string",

}
```

## 1.2 Login to Account - `/users/login` (POST)
Users Login to their Account

**Request**:

```json
{
    "name": "string",
    "username": "string",
    "email": "string",
    "password": "string",

}
```

## 1.3 Logout of Account - `/users/logout/{user_id}` (POST)
Users log out of their account

**Request**:

```json
{
    "user_id": "integer",
}
```


# 2. Get Shoe Info

## 2.1. Get Shoe - `/shoes/{shoe_id}` (GET)

Returns shoe info for the shoe you are looking at

**Request**:

```json
{
    "shoe_id": "integer",
    "shoe_name": "string",
    "brand": "string",
    "fit": "string",
    "retail_price": "integer",
    "num_reviews": "integer",
    "rating": "integer"
}
```

# 3. Leave Rating

## 3.1 Leave Rating - `/shoes/{shoe_id}/review/{user_id}` (POST)
Creates a new rating for a specific shoe.

**Request**:

```json
{
    "rating": "integer",
    "comments": "string",
    "username": "string"
}
```

# 4. View Ratings

## 4.1 Get Reviews  - `/shoes/{shoe_id}/reviews` (GET)
Returns all reviews and their contents for a certain shoe

**Returns**:

```json
[
    {
        "rating": "integer",
        "comments": "string",
        "username": "string"
    }
]
```

## 4.2 Get Reviews  - `/users/{user_id}/reviews` (GET)
Returns all reviews and their contents for a certain shoe

**Returns**:

```json
[
    {
        "user_id": "integer"
    }
]
```

# 5. Search

## 5.1 Search Shoe - `/shoes/search/` (GET)
Returns shoes that match your search value

**Request**:
```json
{
    
    "search_value": "string", 
}
```

**Returns**:
```json
[
  "previous": "integer",
  "next": "integer",
  "results": 
    [
    {
        "shoe_id": "integer"
        "shoe_name": "string", 
        "brand": "string",
         "rating": integer
    },...
    ]
]
```

## 5.2 Search Users - `/users/search/` (GET)
Returns users based on your search

**Request**:
```json
{
    "search_value": "string", 
}
```

**Returns**:
```json
{
  "previous": "",
  "next": "",
  "results": [
    {
        "username": "string"
    },...
    ]
}
```

# 6. Post Shoe

## 6.1 Post Shoe - `/shoes/{shoe_id}` (POST)

Adds new shoe to website

**Request**:

```json
{
    "shoe_name": "string",
    "brand": "string",
    "fit": "string",
    "retail_price": "integer",
}
```

# 7. User Shoes Catalog

## 7.1 Add Shoe to Catalog - `/users/{user_id}/shoes/{shoe_id}` (POST)

Adds requested shoe to your profile shoe collection

**Request**:

```json
{
    "shoe_id": "integer",
    "user_id": "integer"
}
```
## 7.2 Add Shoe to Catalog - `/users/{user_id}/shoes` (POST)
Adds requested shoe to your profile shoe catalog

**Request**:

```json
{
    "user_id": "integer"
}
```

# 8. Get Account Info:

## 8.1. Get Account Catalog - `/users/{user_id}/catalog` (GET)

Returns information of the user profile you're viewing

**Returns**:
```json
[
    {
        "shoe_id": "integer"
        "shoe_name": "string", 
        "brand": "string",
        "rating": integer
    }

]
```

# 9. Get Entire Shoe Catalog:

## 9.1. Get Shoe Catalog - `/shoes` (GET)

Returns shoe catalog of the entire website's shoe library.

**Returns**:
```json
[
    {
        "name": "string", 
        "brand": "string",
        "avg_rating": "integer"
    }
]

```

# 10. Shoe Comparison

## 10.1 GET Shoe Comparison - `/shoes/compare/{shoe_id_1}/{shoe_id_2}` (GET)

Initiates a comparison between two shoes
**Requests**
```json
{
    "shoe_id_1": "integer",
    "shoe_id_2": "integer",
}
```

**Returns**:
``` json

{
    "shoe_ids": ["integer", "integer"],
    "shoe_names": ["string","string"],
    "brands": ["string","string"],
    "fits": ["string","string"],
    "retail_prices": ["integer","integer"],
    "ratings": ["integer","integer"],
}
```

# 11. Brands

## 11.1 Create Brand Account  - `/brands/` (POST)
Brands create a brand account.

**Requests**
```json
{
    "brand_name": "string",
    "email": "string",
    "password": "string"
}
```

## 11.2 Brand POSTS Shoe  - `/shoes/compare/{shoe_id_1}/{shoe_id_2}` (POST)

**Requests**
```json
{
    "shoe_name": "string",
    "brand": "string",
    "price": "integer",
    "color": "string",
    "material": "string",
    "type": "string"
}
```

