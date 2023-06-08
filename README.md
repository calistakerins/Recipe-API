<h1 align="center">
  <a href="https://github.com/calistakerins/Recipe-API">
    <!-- Please provide path to your logo here -->
    <img src="docs/images/logo.svg" alt="Logo" width="100" height="100">
  </a>
</h1>

<div align="center">
  Recipe_API
  <br />
  <a href="#about"><strong>Explore the screenshots »</strong></a>
  <br />
  <br />
  <a href="https://github.com/calistakerins/Recipe-API/issues/new?assignees=&labels=enhancement&template=02_FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
  .
  <a href="https://github.com/calistakerins/Recipe-API/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>
</div>

<div align="center">
<br />

[![Pull Requests welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg?style=flat-square)](https://github.com/calistakerins/Recipe-API/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
[![made with hearth by Anna Rosenberg, Michelle Tan and Calista Kerins](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-GITHUB_USERNAME-ff1414.svg?style=flat-square)](https://github.com/annarosenberg-lab)

</div>

<details open="open">
<summary>Table of Contents</summary>

- [About](#About)
  - [Usage](#usage)
  - [Built With](#built-with)
- [Prerequisites](#prerequisites)
- [Technical Specification and Documentation](#Technical-Specification-and-Documentation)
- [Roadmap](#roadmap) 
- [Support](#support)
- [Security](#security)
- [Acknowledgements](#acknowledgements)

</details>

---

## About

> **[?]**
> This API simulates a recipe database. Users can access information about recipes, costs of ingredients, ingredient amounts, meal types, and more. This database serves to help people find the right recipes for their lifestyles. If the user wants to make something of a certain cuisine or have something with a certain number of calories, these parameters can be referenced. They can also favorite a recipe to access a certain recipe easily. Recipes can be added and ingredients of recipes can be modified if a user wants to change a certain ingredient. 

<details>
<summary>Screenshots</summary>
<br>

> **[?]**
> Please provide your screenshots here.

|                               Home Page                               |                               Login Page                               |
| :-------------------------------------------------------------------: | :--------------------------------------------------------------------: |
| <img src="docs/images/screenshot.png" title="Home Page" width="100%"> | <img src="docs/images/screenshot.png" title="Login Page" width="100%"> |

</details>

## Usage

> **[?]**
Our API is currently running on Vercel. Below you can find a link to our production API.

-Production: https://recipe-api-peach.vercel.app/

### Built With

> **[?]**
- Supabase
- Vercel CLI 

### Prerequisites

> **[?]**
- fastapi==0.88.0
- pytest==7.1.3
- uvicorn==0.20.0
- sqlalchemy==2.0.7
- psycopg2-binary~=2.9.3
- Python-dotenv
- Pre-commit
- Supabase
- Faker
- numpy


### Technical Specification and Documentation

> **[?]**
> Describe how to install and get started with the project.
- Endpoint Documentation: https://github.com/calistakerins/Recipe-API/blob/main/Endpoint_Documentation%20(1).pdf
- ER Diagram: https://github.com/calistakerins/Recipe-API/blob/main/Recipe%20API%20ER%20Diagram%20(3).pdf
- Documentation of Complex Transactions with Concurrency: https://github.com/calistakerins/Recipe-API/blob/main/Complex_Transactions_Write_Up.pdf


## Roadmap

> **[?]**
See the [open issues](https://github.com/calistakerins/Recipe-API/issues) for a list of proposed features (and known issues).

- [Top Feature Requests](https://github.com/calistakerins/Recipe-API/issues?q=label%3Aenhancement+is%3Aopen+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Top Bugs](https://github.com/calistakerins/Recipe-API/issues?q=is%3Aissue+is%3Aopen+label%3Abug+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Newest Bugs](https://github.com/calistakerins/Recipe-API/issues?q=is%3Aopen+is%3Aissue+label%3Abug)

## Support

> **[?]**
> Provide additional ways to contact the project maintainer/maintainers.

Reach out to the maintainer at one of the following places:

- arosen12@calpoly.edu
- [GitHub issues](https://github.com/calistakerins/Recipe-API/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+)

## Security

> **[?]**
Recipe-API follows good practices of security, but 100% security cannot be assured.
Recipe-API is provided **"as is"** without any **warranty**. Use at your own risk.

## Acknowledgements

> **[?]**
> Thank you to these awesome resources that were used during the development of Recipe-API
> https://github.com/jackalnom/movie_api
