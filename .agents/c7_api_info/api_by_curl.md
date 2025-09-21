# Context7 API Documentation by way of cURL

Setup
```bash
CONTEXT7_API_KEY='your_api_key_here'
BASEURL='https://context7.com/api/v1'
AUTHN_HEADER="Authorization: Bearer $CONTEXT7_API_KEY"
```

## Start with a search

### Request
```bash
QP_QUERY='query=mcp+sdk+with+sse'
curl -X GET --url "$BASEURL/search?$QP_QUERY" -H "$AUTHN_HEADER"
```

### Response
There will be more than one result -- only one is shown here for brevity. 
The value of "id" fields should be noted for follow-up fetches.
```json
{
    "results": [
        {
            "id": "/mybigday/mcp-sdk-client-ssejs",
            "title": "Model Context Protocol SDK Client SSE.js",
            "description": "A client transport alternative for the Model Context Protocol SDK, based on sse.js, designed to work with React Native and support Streamable HTTP and SSE.",
            "branch": "main",
            "lastUpdateDate": "2025-07-04T22:48:46.861Z",
            "state": "finalized",
            "totalTokens": 837,
            "totalSnippets": 4,
            "totalPages": 1,
            "stars": 0,
            "trustScore": 9.3,
            "versions": []
        }
    ]
}
```


## Follow it up with one or more fetches

### Request
Use the "id" value from the search result as the {context7CompatibleLibraryID}

```bash
QP_TYPE='type=text'
QP_TOKENS='tokens=10000' # max tokens that will be returned. suggested range 5000-15000
QP_TOPIC='topic=sse' # intra-library area of interest (optional)
PP_ID='/mybigday/mcp-sdk-client-ssejs' # from search result
curl -X GET --url "$BASEURL/$PP_ID?$QP_TYPE&$QP_TOKENS&$QP_TOPIC" -H "$AUTHN_HEADER"
```

### Response
```text
...Information extracted from the documentation of the library in text/markdown format...
```
