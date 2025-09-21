# c7fetch Implementation Plan

## Project Overview
c7fetch is a CLI tool for exploring and retrieving Context7 documentation for offline use. The tool provides commands for configuration, searching, reviewing search results, and fetching documentation.

## Current State
The project has a basic structure with:
- ✅ **Complete**: Configuration management (`config` module)
- ❌ **Incomplete**: Search functionality (`search` module)
- ❌ **Incomplete**: Fetch functionality (`fetch` module)
- ❌ **Incomplete**: Review functionality (`review` module)
- ❌ **Incomplete**: API client (`c7/api.py`)

## Core Features to Implement

### 1. Context7 API Client (`c7/api.py`)
The foundation for all API interactions with Context7.

**Required Methods:**
- `search(query: str) -> dict`: Execute search queries against the Context7 API
- `fetch_docs(library_id: str, tokens: int, format: str, topic: str = None) -> str`: Fetch documentation for a specific library
- Authentication handling using Bearer token
- Error handling for API responses
- Rate limiting support (using request_delay setting)

### 2. Search Command (`cli/search.py`)
Allows users to search Context7 and save results to JSON files.

**Features:**
- Execute single or multiple searches (pipe-separated queries)
- Auto-generate filenames based on query
- Save results to configurable directory (`search_dir` setting)
- Support for overwrite protection (`no_overwrite` setting)
- Display search result summary after completion

### 3. Review Command (`cli/review.py`)
Provides a formatted view of search results to help users decide what to fetch.

**Features:**
- Display search results in rich tables
- Support filtering by:
  - Library ID glob pattern
  - Title/description glob pattern
  - Specific search result files
- Option to merge results from multiple search files
- Columns: Library ID, Title, Last Updated, Stars, Trust Score, Description

### 4. Fetch Command (`cli/fetch.py`)
Downloads documentation from Context7 based on search results.

**Features:**
- Fetch docs by library ID (with glob support)
- Optional title/description filtering
- Configurable token count
- Support for text (markdown) or JSON format
- Auto-generate filenames and organize in library-specific directories
- Overwrite protection

## Implementation Order

### Phase 1: Core API Functionality
1. Implement Context7 API client with basic authentication
2. Add search method with proper error handling
3. Add fetch method with format support
4. Test API client with sample queries

### Phase 2: Search Command
1. Implement single search functionality
2. Add multi-search support (pipe-separated)
3. Implement file saving with auto-naming
4. Add result summary display

### Phase 3: Review Command
1. Implement JSON file reading
2. Create rich table formatting
3. Add glob filtering for library IDs
4. Add title/description filtering
5. Implement merge functionality

### Phase 4: Fetch Command
1. Implement basic fetch with library ID
2. Add glob pattern support
3. Add filtering by title/description
4. Implement file organization and naming
5. Add format selection support

## Technical Considerations

### Dependencies
- `requests`: For HTTP API calls
- `typer`: CLI framework (already integrated)
- `rich`: For formatted console output
- `pathvalidate`: For safe filename generation (mentioned in README)
- `glob` or `fnmatch`: For pattern matching

### File Organization
```
c7docs/
├── search/
│   ├── query1.json
│   └── query2.json
└── {library_id}/
    └── {auto_named_file}.md
```

### Error Handling
- API authentication failures
- Network errors
- Invalid search queries
- File system errors (permissions, disk space)
- Invalid configuration

### Testing Strategy
- Unit tests for API client
- Integration tests for CLI commands
- Mock API responses for testing
- File system operation tests

## Potential Enhancements (Future)
- Caching mechanism for repeated searches
- Parallel fetching for multiple documents
- Progress bars for long-running operations
- Export to different formats (PDF, HTML)
- Incremental updates for previously fetched docs
- Search result deduplication