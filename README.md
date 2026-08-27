# ng-address-toolkit

A simple Python package for Nigerian address data. It gives you states, LGAs (Local Government Areas), wards, and towns, all in one place, with no API calls and no internet needed.

## Who is this for

This package is for anyone building software that needs to work with Nigerian locations, including:

- Backend and full stack developers building signup forms, checkout flows, or KYC forms that ask for a Nigerian address
- Fintech and e-commerce teams that need to validate or standardize customer addresses
- Logistics and delivery platforms that need to map a location to its state, LGA, or ward
- Data teams building dashboards or reports that need to group data by Nigerian administrative regions
- Anyone building a "select your state" or "select your LGA" dropdown and tired of typing the list out by hand

If you need structured, ready to use Nigerian states, LGAs, wards, or town data in a Python project, this package is for you.

## Installation

```bash
pip install ng-address-toolkit
```

## Quick start

```python
from ng_address_toolkit import get_states, get_lgas_by_state, search

# Get every state
states = get_states()
print(states[0])
# {'code': 'AB', 'name': 'Abia', 'capital': 'Umuahia', ...}

# Get all LGAs in Lagos
lagos_lgas = get_lgas_by_state("LA")
for lga in lagos_lgas:
    print(lga["name"])

# Search across everything
results = search("ikeja")
print(results)
```

That's it. All the data ships with the package, so calls like `get_states()` return instantly with no network request.

## Data structure

The package organizes Nigerian location data into four levels:

```
State -> LGA -> Ward -> Town
```

Each level is a plain Python list of dictionaries. Here is what to expect from each one.

### State

```python
{
    "code": "LA",
    "name": "Lagos",
    "capital": "Ikeja",
    "region": "South West",
    "latitude": 6.5244,
    "longitude": 3.3792
}
```

### LGA

```python
{
    "alias": "ikeja",
    "name": "Ikeja",
    "state_code": "LA",
    "latitude": 6.6018,
    "longitude": 3.3515
}
```

### Ward

```python
{
    "alias": "alausa",
    "name": "Alausa",
    "lga_alias": "ikeja",
    "state_code": "LA",
    "postal_code": "100271",
    "latitude": 6.6058,
    "longitude": 3.3541
}
```

Note that `latitude` and `longitude` are optional on a ward. Some wards may not have coordinates.

### Town

```python
{
    "name": "Opebi",
    "ward_alias": "alausa",
    "lga_alias": "ikeja",
    "state_code": "LA",
    "latitude": 6.5931,
    "longitude": 3.3608
}
```

## Functions

### get_states()

Returns a list of every state in Nigeria.

```python
from ng_address_toolkit import get_states

states = get_states()
print(len(states))  # 37 (36 states plus the FCT)

for state in states:
    print(state["name"], state["code"])
```

### get_lgas()

Returns a list of every LGA in the country.

```python
from ng_address_toolkit import get_lgas

lgas = get_lgas()
print(len(lgas))  # 774
```

### get_wards()

Returns a list of every ward.

```python
from ng_address_toolkit import get_wards

wards = get_wards()
print(wards[0])
```

### get_towns()

Returns a list of every town and settlement.

```python
from ng_address_toolkit import get_towns

towns = get_towns()
print(towns[0])
```

### get_lgas_by_state(state_code)

Returns only the LGAs that belong to a given state. The state code is not case sensitive.

```python
from ng_address_toolkit import get_lgas_by_state

kano_lgas = get_lgas_by_state("KN")
# also works
kano_lgas = get_lgas_by_state("kn")

for lga in kano_lgas:
    print(lga["name"])
```

If the state code does not exist, you simply get back an empty list.

### get_wards_by_lga(lga_alias)

Returns only the wards that belong to a given LGA. The LGA alias is not case sensitive.

```python
from ng_address_toolkit import get_wards_by_lga

wards = get_wards_by_lga("ikeja")
for ward in wards:
    print(ward["name"])
```

### search(query, level="all")

Searches for a location by name. Matching is a simple, case-insensitive substring match, not a fuzzy search. This means the spelling has to be correct. For example, searching `"ikej"` will not match `"Ikeja"`, but `"ikeja"` will.

By default it searches across states, LGAs, wards, and towns all at once.

```python
from ng_address_toolkit import search

# Search everywhere
results = search("lagos")

# Search only within states
results = search("lagos", level="state")

# Search only within LGAs
results = search("ikeja", level="lga")

# Search only within wards
results = search("alausa", level="ward")

# Search only within towns
results = search("opebi", level="town")
```

Valid values for `level` are `"all"`, `"state"`, `"lga"`, `"ward"`, and `"town"`.

Calling `search()` with an empty string, or a string that is just spaces, raises a `ValueError`:

```python
search("")       # raises ValueError
search("   ")    # raises ValueError
```

Calling `search()` with an invalid `level` also raises a `ValueError`, and the error message tells you which values are valid:

```python
search("lagos", level="country")
# ValueError: Invalid level 'country'. Valid options are: all, lga, state, town, ward
```

## What you can build with it

You can use the hosted API directly without setting up or running the project yourself.

Visit the [home page](https://ng-address-api.vercel.app/) to explore the API and start making requests.

- Address forms with cascading dropdowns for state, LGA, and ward
- Address validation and normalization for checkout or signup flows
- Delivery zone and logistics tools that map a town or ward to its LGA and state
- Location-based search and autocomplete for Nigerian addresses
- Reports and analytics that group users or orders by state, LGA, or region

## License

MIT
