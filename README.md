# c7fetch

c7fetch is a CLI tool to explore and retrieve context7 docs for offline use.

## Usage:

```python
# Set, view, and unset configuration options
c7fetch config [-h|--help]

# Perform a search and save the results to a json file
# By default the path will be ./c7docs/search/{autonamed_from_query}.json
c7fetch search <query>

# shorthand for running 2+ searches as a single command, generates 2+ search result json files
c7fetch search <query1>|<query2>

# Prints a summary of search results so you can decide what to fetch
# Considers all search result json files by default
c7fetch review [library_id_glob] [title_and_desc_glob]
    ... -f <search_result_json_file> ...
    ... --merge ... # don't break out review tables by search result file

# Fetch documents by library_id and optional title/description filter
# By default saves to ./c7docs/{library_id}/{autonamed_from_query}.md
# default format is text (markdown)
# default tokens can be configured via `c7fetch config`
c7fetch fetch [--tokens n] [--format <text|json>] <query> <library_id_glob> [title_and_desc_glob]
```

## Automatic file naming

c7fetch attempts to automatically name the files it saves. To ensure that it does not attempt to 
use characters that are invalid in filenames, it uses the [pathvalidate] library. Also, spaces
are replaced with underscores.

Output files are automatically overwritten. You can turn off this behavior with the `no_overwrite` setting.

[pathvalidate]: https://github.com/thombashi/pathvalidate