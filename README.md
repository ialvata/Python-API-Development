# Python-API-Development

[![alt text][image]][hyperlink]

[hyperlink]: https://youtu.be/0sOvCWFmrtA
[image]:
https://github.com/ialvata/Python-API-Development/assets/110241614/6ee51d95-4301-4857-9765-5784aa2d1548
(Screenshot of YouTube Video Course)




This will be my interpretation of the Python API Development 20h course from Sanjeev Thiyagarajan on Youtube. :) 

[Link to YouTube](https://www.youtube.com/watch?v=0sOvCWFmrtA&ab_channel=freeCodeCamp.org)



## Pre-Commit Hooks
- Black:Python code formatter. Character line length optimised for my screen.
- Flake8: Analyses your code without actually running it. It checks for errors, enforces a coding standard, looks for code smells, and can make suggestions about how the code could be refactored. Initially, this repo used pylint, but when using an ORM like SQLAlchemy, pylint is too slow.
- isort: Python utility / library to sort imports alphabetically, and automatically separated into sections and by type.

## Pytest
- One thing that could be improved was leaving the pytest tests until the end... In my opinion, Sanjeev should have introduced the tests much earlier, and as he created the new methods, or operations, he could have explained a bit how to create useful tests.

## Grafana
- Allows us to query, visualize, alert on and understand our metrics from different data sources, all through creating our own dashboards. Currently, we're only connected to the PostgreSQL docker container.
- Prometheus and cAdvisor for containers metrics capture have been added. TODO: Create an integration with Grafana.
- TODO: Put a Grafana Loki integration up and running.
