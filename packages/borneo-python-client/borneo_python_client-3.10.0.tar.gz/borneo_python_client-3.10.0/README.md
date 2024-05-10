## Borneo_python_client Client

borneo_python_client client

### Documentation

# Overview

The Borneo API v3 provides a set of RESTful APIs to query and manage the
Borneo Inventory and Catalog, and to schedule data scans and retrieve scan
results. Request and response payloads are JSON documents.

## API Endpoint

The API endpoint for the Borneo API is hosted on the same domain as the Borneo Dashboard, under the `/api/` path.

```
https://demo.app.borneodata.com/api/
```

## Authentication

Requests to the Borneo API must be authenticated using an authentication token. The token is passed in the `Authorization` header of the request.

```
Authorization: Bearer <token>
```

**TODO**: Explain how to obtain the authentication token.

## Pagination

All list operations support pagination. The `pageSize` parameter can be
used to control the number of results returned per API request. If there
are more results available, the API response will contain a `nextToken`
value that can be used to retrieve the next page of results by passing it
as the `nextToken` parameter in a subsequent API request.
