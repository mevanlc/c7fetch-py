# c7fetch

c7fetch is a CLI tool to explore and retrieve context7 docs for offline use.

## Usage:

```bash
# Set, view, and unset configuration options
c7fetch config [-h|--help]

# Perform a search and save the results to a json file
# By default the path will be ./c7docs/search/{autonamed_from_query}.json
c7fetch search "<query>"

# shorthand for running 2+ searches as a single command, generates 2+ search result json files
c7fetch search "<query1>|<query2>"

# Prints a summary of search results so you can decide what to fetch
c7fetch review "<library_id_glob>" "[]
c7fetch fetch "<library_id_glob>"
```
