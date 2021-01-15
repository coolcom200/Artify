# Artify

## Installation

1. Ensure that `Docker`, `docker-compose` and `python3` are installed on your machine
2. Run `docker-compose up`
3. In another shell instance navigate to the `api` directory
4. To initialize the Elasticsearch Indices run `python3 init_db.py` wait until
   the script
   outputs that the indices have been created.
5. The services should all be up and running

### Running After Installation

1. Run `docker-compose up` and wait until the logging outputs that the:
   `Cluster health has changed from [RED] to [GREEN]` as shown below
   ```
   elasticsearch    | {"type": "server", "timestamp": "XXX", "level": "INFO", "component": "o.e.c.r.a.AllocationService", "cluster.name": "docker-cluster", "node.name": "XXX", "message": "Cluster health status changed from [RED] to [GREEN] (reason: [shards started [[image-products][0]]]).", "cluster.uuid": "XXX", "node.id": "XXX"  }
   ```
   XXX used denote extra information

## Description of Services Running

## API - http://localhost:5000

The api can also be accessed on http://locahost/api which is just proxied
to http://localhost:5000

### Endpoints
- Examples use cURL with `-i` to provide the HTTP response headers in the output
#### Register

- Used to create an account for use with the image repository returns `200` and
  a session cookie if the request is successful

Example usage:

```bash
curl -i 'http://localhost/api/register' -H 'Content-Type: application/json' --data-raw '{"email":"test@user.ca","password":"supersecret","name":"Test User"}' -c cookies.txt
```

Example error:

```
{
    "error_message": "Password is required"
}
```

#### Login

- Used to login to a registered account returns `200` and a session cookie if
  the request is successful

Example usage:

```bash
curl -i 'http://localhost/api/login' -H 'Content-Type: application/json' --data-raw '{"email":"test@user.ca","password":"supersecret"}' -c cookies.txt
```

Example error:

```
{
    "error_message": "Password is required"
}
```

#### Create Product

- Used to create a new product. Returns `200` if successful otherwise returns
  `400` and an error message or a `403` if you are not authenticated

Example usage:

```bash
 curl -i 'http://localhost/api/create' -F "title=ABC" -F "visibility=Public" -F "price=1234" -F "description=Test123" -F "files=@/PATH_TO_FILE.png" -b cookies.txt -c cookies.txt
```

Example error:

```
{
    "error_message": "A title is required"
}
```

#### Search

- Used to search for visible products. Supports limiting searches by
  price and by query text. Returns an array of matching products.

Example usage:

```bash
curl -i 'http://localhost/api/search?query=Logo&price_min=5&price_max=12'
```

#### Get Image

- Used to retrieve images from the storage system.

Example usage (change the UUID):

```bash
curl 'http://localhost/api/image/1b640668-ab4c-4db1-84f9-9698e2068dcc/' > out
```
## Frontend - http://localhost

- This hosts a static set of pages to enable testing of the API in a more easy
  fashion
- Upon loading the page for the first time there will be an empty white screen.
  This is as there are no products added to the database. To add products:

  - Using the top navbar navigate to `Account > Create Account` fill in the
    signup form and submit
  - After submitting the page you should be redirected to the `Create Product`
    page
  - Fill in the form to create a product
  - Afterwards, navigate to http://localhost
  - Your newly added item should be visible (assuming visibility was set to
    Public)

- Additionally, there is a search feature allowing for filtering the products by price and by title and description

## Elasticsearch - http://localhost:9200

- All the data about the users and products are stored and indexed in Elasticsearch

## Things to Improve

- Web is mainly just for testing the API. As a result, it doesn't dynamically
  respond to the user being logged in

- Support for chunking uploads to allow very large files to be uploaded

- Use JWT to handle authentication instead of session cookies

- Pagination of results

- Add better documentation of the API

- Initialize database indices with a different method

- Add support to display multiple images on web app (backend supports multiple
  images per product)