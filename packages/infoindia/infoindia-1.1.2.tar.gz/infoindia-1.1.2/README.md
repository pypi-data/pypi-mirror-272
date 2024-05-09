# INFOINDIA

infoindia is a wrapper for [STATE DATA APIs](https://apis.travelrealindia.com).

## API KEY

Create a user [here](https://apis.travelrealindia.com/create_user) to get your api_key

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install infoindia.

```bash
pip install infoindia
```

## Usage

```python
import infoindia as ind

# set 'api_key'
ind.set_api_key("xxxxxxxxxxxxAPI_KEYxxxxxxxxxxx")

# initialize state var
WB = ind.State('WB')

# fetch state data
WB.fetch()

# fetch all cities in state 
WB.fetch_cities()

# initialize ut var
PY = ind.UT('PY')

# fetch state data
PY.fetch()

# fetch all cities in UT 
PY.fetch_cities()

# initialize city var
SLG = ind.City('WB019')

# fetch city data
SLG.fetch()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)