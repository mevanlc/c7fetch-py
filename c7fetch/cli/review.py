from . import typer_util

app = typer_util.TyperAlias(module=__name__)

"""
{
  "results": [
    {
      "id": "/websites/react_dev",
      "title": "React",
      "description": "React is a JavaScript library for building user interfaces. It allows developers to create interactive web and native applications using reusable           ↪components, enabling efficient and scalable UI development.",
      "branch": "main",
      "lastUpdateDate": "2025-08-30T17:48:56.092Z",
      "state": "finalized",
      "totalTokens": 391665,
      "totalSnippets": 1752,
      "totalPages": 193,
      "stars": -1,
      "trustScore": 8,
      "versions": []
    },
    /* ...etc... */
  ]
}
"""

# table printout like ( use rich table )
"""

            Results from: path/to/search_results.json
            Query: "react|vuejs|angular"

| Library ID          | Title  | Last Updated        |  Stars | Trust    | Description (truncated for terminal)         |
|---------------------|--------|---------------------|--------|----------|----------------------------------------------|
| /websites/react_dev | React  | 2025-08-30 17:48:56 |   2813 |       80 | React is a JavaScript library for building   |
| /websites/vuejs     | Vue.js | 2025-08-30 17:48:56 |   3893 |       75 | Vue.js is a progressive JavaScript framew... |
| /angular/angular    | Angular| 2025-08-30 17:48:56 |   2451 |       78 | Angular is a platform and framework for bu...|


            Results from: path/to/search_results2.json
            Query: "someethingelse"

| Library ID          | Title  | Last Updated        |  Stars | Trust    | Description (truncated for terminal)         |
|---------------------|--------|---------------------|--------|----------|----------------------------------------------|
| /websites/react_dev | React  | 2025-08-30 17:48:56 |   2813 |       80 | React is a JavaScript library for building   |
| /websites/vuejs     | Vue.js | 2025-08-30 17:48:56 |   3893 |       75 | Vue.js is a progressive JavaScript framew... |
| /angular/angular    | Angular| 2025-08-30 17:48:56 |   2451 |       78 | Angular is a platform and framework for bu...|
"""
