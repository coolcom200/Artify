<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/coolcom200/Artify">
    <img src="docs/logo.png" alt="Logo" width="100" height="100">
  </a>

<h3 align="center">Artify</h3>

  <p align="center">
    A GraphQL Image Repository API
    <br />
    <a href="#api-details"><strong>Usage</strong></a> 
  </p>
</p>

<h2 style="display: inline-block">Table of Contents</h2>
<ol>
  <li><a href="#about-the-project">About The Project</a></li>
  <li><a href="#getting-started">Getting Started</a></li>
  <li><a href="#api-details">API Details</a></li>
  <li><a href="#discussion">Discussion</a></li>
  <li><a href="#improvements">improvements</a></li>
</ol>

## About The Project

This is a GraphQL API that is designed as a basic image repository. It enables
users to create an account and upload images and have them available for sale.
It's like Kijiji--only simplified.

The first version of this API utilized Elasticsearch as the database. However, a
PostgreSQL database has been added. As a result, the application is now designed
to work with two different database technologies.

### Built With

- [GraphQL](https://graphql.org/)
- [Ariadne](https://ariadnegraphql.org)
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Elasticsearch](https://www.elastic.co/elastic-stack)
- [PostgreSQL](https://www.postgresql.org/)

## Getting Started

### Prerequisites

This project requires the following tools:

- Docker
- Docker Compose

Please make sure that you have these installed.

### Installation & Starting the system

To clone this project run:

`git clone https://github.com/coolcom200/artify.git`

To start the API, navigate into the repository you just cloned and run:
`docker-compose up`

Note: After starting the application wait around 30 seconds to ensure that every
service has started correctly.

## Configuration

Since this project has two different databases available, switching between the
two is handled using a configuration file. By default the API is using a
PostgreSQL database. In order to change the API to use Elasticsearch, the
following changes are required:

In the `api/config.json` file:

1. the `DATABASE_TYPE` needs to be changed to `elasticsearch`
2. the `DATABASE_HOST` needs to be changed to `elasticsearch` (
   since `elasticsearch` is the name of the docker-compose service running
   Elasticsearch)
3. the `DATABASE_PORT` needs to be changed to `9200`

In `docker-compose.yml` the `postgres` service can be commented out or removed
and in its place the `elasticsearch` service should be added:

```YAML
# docker-compose.yml
services:
   # ... Other services ...
   elasticsearch:
      image: docker.elastic.co/elasticsearch/elasticsearch:7.10.1
      container_name: elasticsearch
      environment:
         - discovery.type=single-node
      expose:
         - 9200
      volumes:
         - elasticsearch-data:/usr/share/elasticsearch/data

# The elasticsearch volume should also be added
volumes:
   elasticsearch-data:
      driver: local
```

In addition make sure to update the `web` service's `depends_on` details to
remove `postgres` and add `elasticsearch`
see [All services docker compose](#all-services-docker-compose) for
a `docker-compose.yml` file with all the database technologies

## API Details

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/c4861540b751a620558f)

[View the API Postman hosted API documentation](https://documenter.getpostman.com/view/14969227/Tz5s4GHW)

The API is running on [localhost:5000/graphql](localhost:5000/graphql) and has
the GraphQL Playground enabled

> :warning: Since the application uses session cookie based authentication you
> should change the playground settings to include credentials in requests. To
> do so change `"request.credentials": "omit"` to `"request.credentials": "include"`

Initially the application has no data and needs to be populated with some data.
To do so create an account and then create a product. Details for how to do so
are documented below.

### Register Mutation

Creates an account. An account is required to create products, and see your
products.

```
mutation {
  register(
    input: { name: "My Name", email: "test@test.ca", password: "mypassword" }
  ) {
    message
  }
}
```

### Login Mutation

To log into your account

```
mutation {
  login(input: { email: "leon@test.ca", password: "123" }) {
    message
  }
}
```

### Logout Mutation

To log out of your account

```
mutation {
  logout {
    message
  }
}
```

### Create Product Mutation

The `createProduct` mutation is responsible for uploading images that are
associated with the product. I haven't found a way to upload images using the
Playground however it is possible using cURL
and [Postman](https://app.getpostman.com/run-collection/c4861540b751a620558f).
This is a protected endpoint so you will need to include cookies in the requests

cURL: Replace anything in the `input: {...}` with your own values and provide a
cookie and an image to upload

```
curl --location --request POST 'http://localhost:5000/graphql' \
--header 'Cookie: session=<COOKIE> \
--form 'map="{\"0\": [\"variables.input.files.0\"]}"' \
--form '0=@"/path/to/file"' \
--form 'operations="{ \"query\":
\"mutation ($input: CreateProductInput!) { createProduct(input: $input) { uid } }\",
\"variables\": {
  \"input\": {
    \"files\": [null],
    \"productName\": \"<PRODUCT NAME>\",
    \"description\": \"<DESCRIPTION>\",
    \"price\": 0.00,
    \"isVisible\": true} } }"'
```

The mutation follows the specification defined in
https://github.com/jaydenseric/graphql-multipart-request-spec

### Search Query

To search for products. All parameters are optional. Avalible parameters
are: `minPrice`, `maxPrice` and `searchQuery`

```
{
  search(minPrice: 2) {
    productName
    owner {
      uid
    }
    price
    images {
      filePath
      fileName
    }
  }
}
```

### Me Query

To get information about the user

```
{
  me {
    email
    uid
    name
    products {
      productName
    }
  }
}
```

### Download Image

To download an image from the API replace the `<UUID>` with an image id.

`curl 'http://localhost/api/image/<UUID>/' > out`

For example:
`curl 'http://localhost/api/image/1b640668-ab4c-4db1-84f9-9698e2068dcc/' > out`

## Discussion

Ariadne, the GraphQL library, was chosen since it is a schema first library
meaning that in the future if this schema needs to be shared with other services
it can be done so in a simple manner. Since Ariadne was being used with Flask it
didn't have an official Flask GraphQL file upload handler, so I wrote one based
on the
[specifications](https://github.com/jaydenseric/graphql-multipart-request-spec)
and a similar handler that was included with Ariadne.

Adding support for multiple databases was tricky as it required custom data
models for Elasticsearch. In particular, the Elasticsearch model for a product
needed the ability to get the owner of the product. However, since the database
has two indices one for the users and another for the products and files, then
to get a product's owner would require querying the database for the owner. As a
result, I created custom data models that would query the database for missing
data.

### Database Structure

For Elasticsearch there are two indices:

1. Users with the following mapping:

```json
{
   "name": {
      "type": "text"
   },
   "email": {
      "type": "keyword"
   },
   "password": {
      "type": "text",
      "index": false
   }
}
```

2. Products with the following mapping:

```json
{
   "product_name": {
      "type": "keyword"
   },
   "description": {
      "type": "text"
   },
   "owner_id": {
      "type": "keyword"
   },
   "is_visible": {
      "type": "boolean"
   },
   "price": {
      "type": "double"
   },
   "images": {
      // Images are stored per product
      "type": "nested"
   }
}
```

For PostgreSQL there are 3 tables that are shown in the diagram below.

 <img src="docs/diagram.png" alt="tables">

## Things to Improve

- Support chunking uploads to allow very large files to be uploaded

- Use JWT to handle authentication instead of session cookies

- Pagination of results

- Add logging

- Add support for cloud based file storage providers such as S3

- Add unit tests

- Improve download security

- Improve the configuration

- Elasticsearch ORM

- Improved Error Messages

- Deploy it!

## All services docker compose

```yaml
services:
   postgres:
      image: postgres:13-alpine
      restart: always
      environment:
         POSTGRES_PASSWORD: mysecretpassword
         POSTGRES_DB: artify_db
      expose:
         - 5432

   web:
      container_name: image-repository
      build: .
      working_dir: /code/api
      environment:
         - FLASK_APP=./
         - FLASK_ENV=development
      ports:
         - 5000:5000
      volumes:
         - ./:/code
      depends_on:
         - postgres
         - elasticsearch

   elasticsearch:
      image: docker.elastic.co/elasticsearch/elasticsearch:7.10.1
      container_name: elasticsearch
      environment:
         - discovery.type=single-node
      expose:
         - 9200
      volumes:
         - elasticsearch-data:/usr/share/elasticsearch/data

volumes:
   elasticsearch-data:
      driver: local
```
