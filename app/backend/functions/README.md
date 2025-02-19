# Coding challenge - REST API

## Description
Leveraging the REST API developed, a number of API endpoints (under the path "/reports/") have been developed to provide answers to the SQL section of the requirements. 

## Endpoints

### `GET /`
A `hello world` type of endpoint.

### `GET /heartbeat`
This endpoint provides a heartbeat to verify the connection between the backend and the SQL database.

### `GET /tables`
This endpoint delivers a JSON object with all the tables present on the SQL database.

### `GET /tables/{tablename}`
This endpoint queries a table (`tablename`) and returns a data sample of 10 rows.

### `POST /tables/{tablename}`
This endpoint allows the end user to upload their own historical data to a specified table (`tablename`).

### `POST /etl/startProcess`
This endpoint allows the end user to execute an ETL process, using the default SQL database and data pre-loaded on the container, and populate the required tables. This process will perform a deduplication process on the data, keeping the first uploaded rows on each table.

### `GET /etl/check`
This endpoint performs a status check on the ETL process, indicating if it's still running or if it's completed.

### `/reports/...`
These endpoints are described in the [reports README](app/backend/reports/README.md).

## Usage

### Prerequisites
In order to do testing with the provided data, you can find on the `app/backend/input/` folder the CSV files provided by the requirements. They must be loaded into the database before requesting any meaningful metric.

### API documentation
On whichever deployment you prefer, you can always find the Swagger documentation on the [http://your-backend-uri/docs](#null).

### CLI usage
To make requests to the API, you can use a `curl` request such as the following:

```bash
$ curl --request 'GET' \
  'http://your-backend-uri/reports/api-endpoint' \
  --header 'accept: application/json'
```

and you should receive a response like this:

```bash
> {
  "report": "mean hired employees on 2021",
  "results": [
    {
      "mean_hires": 130
    }
  ]
}
```

### Swagger testing
The Swagger documentation allows each and all endpoints to be tested in a graphical, interactive way.

![Swagger docs testing](documentation/image.png)

## Comments, issues and requests

All questions, requests and comments can be placed on the [Issues GitHub page](https://github.com/DarkestAbed/challenge-de-ingestion/issues).

Also, if you want to contribute, you can fork the repo and [send a Pull Request](https://github.com/DarkestAbed/challenge-de-ingestion/pulls).

## TODO: tech debt

- [ ] Supress logging and debugging messages from Icecream
