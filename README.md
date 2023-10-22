# Python-API-Development ([YouTube video](https://www.youtube.com/watch?v=0sOvCWFmrtA&ab_channel=freeCodeCamp.org))

[![alt text][image]][hyperlink]

[hyperlink]: https://youtu.be/0sOvCWFmrtA
[image]:
https://github.com/ialvata/Python-API-Development/assets/110241614/6ee51d95-4301-4857-9765-5784aa2d1548
(Screenshot of YouTube Video Course)

## Overview

| **Open Source** | ![BSD 3-clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)
|---|---|
| **Tech Stack** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white) |


This is my interpretation of the Python API Development 20h course from Sanjeev Thiyagarajan on Youtube. :) 

This project consists in a web app backend of a social message board type. We can create users, with their respective authentication credentials (OAuth 2.0), each user can post messages, and do the usual CRUD type of requests (subject to authentication) regarding the posts. They also have the possibility of voting on posts.

## Integrations

### Linear 
This project is (now) being planned and tracked, using Linear.app. See an example of this integration [here](https://github.com/ialvata/Python-API-Development/pull/11).

### Pre-Commit Hooks
- Black:Python code formatter. Character line length optimised for my screen.
- Flake8: Analyses your code without actually running it. It checks for errors, enforces a coding standard, looks for code smells, and can make suggestions about how the code could be refactored. Initially, this repo used pylint, but when using an ORM like SQLAlchemy, pylint is too slow.
- isort: Python utility / library to sort imports alphabetically, and automatically separated into sections and by type.

### Pytest
One thing that could be improved was leaving the pytest tests until the end... In my opinion, Sanjeev should have introduced the tests much earlier, and as he created the new methods, or operations, he could have explained a bit how to create useful tests.
#### TODO:
- Add coverage report.


### Grafana
Allows us to query, visualize, alert on and understand our metrics from different data sources, all through creating our own dashboards.
PostgreSQL, and Prometheus as grafana's datasources have been added.
 
The dashboard from PostgreSQL was created in an automated way.
![Screenshot from 2023-06-12 20-02-59](https://github.com/ialvata/Python-API-Development/assets/110241614/1605597f-619b-447d-8a03-c0364859ab7d)

The dashboard from Prometheus metrics, in the picture below, was imported manually.
![image](https://github.com/ialvata/Python-API-Development/assets/110241614/74f8cbbe-78c3-4389-abe7-9b8841dc077d)

#### TODO: 
- Put a Grafana Loki integration up and running.
- Improve Prometheus dashboards.

### Prometheus
Prometheus collects and stores its metrics as time series data, i.e. metrics information is stored with the timestamp at which it was recorded, alongside optional key-value pairs called labels.
#### TODO: 
- Add a PostgreSQL exporter to Prometheus docker image.
