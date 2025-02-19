# Coding challenge - reporting data

## Description
Leveraging the REST API developed, a number of API endpoints (under the path "/reports/") have been developed to provide answers to the SQL section of the requirements. 

## Endpoints

### `GET /reports/employeesByQuarter`
This endpoint provides an answer to the requirement 

> Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.

This endpoint will ask for no parameters or inputs; it will execute the calculations exclusively for the year 2021. It will yield a JSON object with the table data, which can be, at a later stage, ingested into any data processing and analysis framework.

### `GET /reports/meanEmployeesHired`
This endpoint will provide the mean number of employees hired across all departments for a specified year. It takes a single parameter, the `year`, and it will deliver a JSON object with the dictionary `results.mean_hires`, containing an integer number (the float answer rounded up).

### `GET /reports/hiringsByDepartment`
This endpoint will provide an answer to the requirement

> List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).

This endpoint will ask for no parameters or inputs; it will execute the calculations exclusively for the year 2021. It will yield a JSON object with the table data, whih can be, at a later stage, ingested into any data processing and analysis framework.

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

- [ ] Use the `year` parameter for all calculations
- [ ] Apply a data quality and hygene framework, such as Great Expectations, to the results
