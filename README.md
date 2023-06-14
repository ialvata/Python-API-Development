# Python-API-Development ([YouTube video](https://www.youtube.com/watch?v=0sOvCWFmrtA&ab_channel=freeCodeCamp.org))

[![alt text][image]][hyperlink]

[hyperlink]: https://youtu.be/0sOvCWFmrtA
[image]:
https://github.com/ialvata/Python-API-Development/assets/110241614/6ee51d95-4301-4857-9765-5784aa2d1548
(Screenshot of YouTube Video Course)




This will be my interpretation of the Python API Development 20h course from Sanjeev Thiyagarajan on Youtube. :) 



## Linear 
This project is (now) being planned and tracked, using Linear.app. See an example of this integration [here](https://github.com/ialvata/Python-API-Development/pull/11).

## Pre-Commit Hooks
- Black:Python code formatter. Character line length optimised for my screen.
- Flake8: Analyses your code without actually running it. It checks for errors, enforces a coding standard, looks for code smells, and can make suggestions about how the code could be refactored. Initially, this repo used pylint, but when using an ORM like SQLAlchemy, pylint is too slow.
- isort: Python utility / library to sort imports alphabetically, and automatically separated into sections and by type.

## Pytest
One thing that could be improved was leaving the pytest tests until the end... In my opinion, Sanjeev should have introduced the tests much earlier, and as he created the new methods, or operations, he could have explained a bit how to create useful tests.
#### TODO:
- Add Tests, and coverage report.

## FastAPI
Sanjeev does not use async functions, but this is encouraged in FastAPI documentation.
#### TODO:
- Convert endpoints to use async functions.

## Grafana
Allows us to query, visualize, alert on and understand our metrics from different data sources, all through creating our own dashboards.
PostgreSQL, and Prometheus as grafana's datasources have been added.
 
The dashboard from PostgreSQL was created in an automated way.
![Screenshot from 2023-06-12 20-02-59](https://github.com/ialvata/Python-API-Development/assets/110241614/1605597f-619b-447d-8a03-c0364859ab7d)

The dashboard from Prometheus metrics, in the picture below, was imported manually.
![image](https://github.com/ialvata/Python-API-Development/assets/110241614/74f8cbbe-78c3-4389-abe7-9b8841dc077d)

#### TODO: 
- Put a Grafana Loki integration up and running.
- Improve Prometheus dashboards.

## Prometheus
Prometheus collects and stores its metrics as time series data, i.e. metrics information is stored with the timestamp at which it was recorded, alongside optional key-value pairs called labels.
#### TODO: 
- Add a PostgreSQL exporter to Prometheus docker image.
