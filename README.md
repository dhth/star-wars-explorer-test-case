# Star Wars Explorer

The project is composed of 3 docker services:
- backend *(Django)*
- client *(React)*
- db *(Postgres)*

## Local Setup
- Prequisites: Docker
- Copy contents of `backend/env.dev.example` into `backend/env.dev`
- Run `docker-compose up -d --build`
- Go to `http://127.0.0.1:3000`

## Backend API

- GET `/fetch-collection` : fetches data from SWAPI people endpoint
- GET `/collections`: returns metadata for stored people collections
- GET `/collections/<id: int>?page_num=<page_num: int>`: returns 10 rows for a specific collection corresponding to page `page_num`
- GET `/collections/value_counts/1?fields=birth_year,homeworld,name`: Returns value counts for a collection based on fields

## Further optimisations
- Asynchronously fetching data (using [asyncio](https://docs.python.org/3/library/asyncio.html)) from remote APIs will quicken up the process since a lot of compute time is being wasted due to network delay. [fastapi](https://fastapi.tiangolo.com/) or any other asynchronous-first web framework would be well suited to handle asynchronous web requests.
- If API pagination length is quite large, data fetch can be split into separate API calls. The current database model has 3 fields which get updated on every data save corresponding to a paginated API response. As such, data fetch could continue from `last_successful_fetch_page`.

    ```python
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    last_successful_fetch_page = models.IntegerField(default=0)
    data_fetch_complete = models.BooleanField(default=False)
    ```
- Data transformations using [pandas](https://pandas.pydata.org/) would be much quicker than `petl`.

## Optional
- Data storage (for person objects) is implemented using both CSV files (mandatory) and postgres (optional). The environment variable `USE_DATABASE_FOR_STORAGE` (False by default) dictates whether data used for rendering the client comes from the file or the database. (comes from the file if `USE_DATABASE_FOR_STORAGE` is False).