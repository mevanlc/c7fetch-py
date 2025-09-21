# TODO Phase 1: Core API Implementation

## Prerequisites
- [ ] Add missing dependency: `pathvalidate` to pyproject.toml
- [ ] Update dependencies: `pip install pathvalidate`
- [ ] Add development dependencies for testing

## Task 1: Implement Context7 API Client
**File:** `c7fetch/c7/api.py`

- [ ] Create Context7Client class
- [ ] Implement authentication with Bearer token
  - [ ] Support direct API key
  - [ ] Support environment variable for API key
- [ ] Implement search method
  - [ ] Accept query parameter
  - [ ] Handle API response
  - [ ] Parse JSON results
  - [ ] Error handling for failed requests
- [ ] Implement fetch_docs method
  - [ ] Accept library_id, tokens, format, topic parameters
  - [ ] Support both text and JSON formats
  - [ ] Handle API response
  - [ ] Error handling
- [ ] Add request delay/rate limiting
- [ ] Add User-Agent header management
- [ ] Implement proper logging
- [ ] Add request timeout handling
- [ ] Write unit tests for API client

## Task 2: Implement Search Command
**File:** `c7fetch/cli/search.py`

- [ ] Implement single search functionality
  - [ ] Parse query argument
  - [ ] Call API client search method
  - [ ] Handle API response
- [ ] Add multi-search support (pipe-separated queries)
  - [ ] Split queries by pipe character
  - [ ] Execute searches sequentially
- [ ] Implement file saving
  - [ ] Auto-generate filename from query
  - [ ] Use pathvalidate for safe filenames
  - [ ] Save to configured search directory
  - [ ] Handle overwrite protection
- [ ] Add result summary display
  - [ ] Show number of results
  - [ ] Display save location
  - [ ] Show basic statistics
- [ ] Add error handling
  - [ ] API failures
  - [ ] File system errors
  - [ ] Invalid queries
- [ ] Write integration tests

## Task 3: Implement Review Command
**File:** `c7fetch/cli/review.py`

- [ ] Implement search result file reading
  - [ ] Find all JSON files in search directory
  - [ ] Parse JSON content
  - [ ] Handle invalid JSON gracefully
- [ ] Create rich table display
  - [ ] Configure table columns
  - [ ] Format dates appropriately
  - [ ] Truncate long descriptions
  - [ ] Handle missing fields
- [ ] Add library ID filtering (glob patterns)
  - [ ] Implement glob matching
  - [ ] Case-insensitive matching option
- [ ] Add title/description filtering
  - [ ] Text search in title/description
  - [ ] Support glob patterns
- [ ] Implement file selection
  - [ ] Accept specific file paths
  - [ ] Validate file existence
- [ ] Add merge functionality
  - [ ] Combine results from multiple files
  - [ ] Remove duplicates
  - [ ] Sort results
- [ ] Add summary statistics
  - [ ] Total results count
  - [ ] Source file information
  - [ ] Filter statistics
- [ ] Write integration tests

## Task 4: Implement Fetch Command
**File:** `c7fetch/cli/fetch.py`

- [ ] Implement basic fetch functionality
  - [ ] Accept query and library_id parameters
  - [ ] Call API client fetch_docs method
  - [ ] Handle API response
- [ ] Add glob pattern support for library_id
  - [ ] Match against search results
  - [ ] Support wildcards
- [ ] Add title/description filtering
  - [ ] Filter results before fetching
  - [ ] Support partial matches
- [ ] Implement file organization
  - [ ] Create library-specific directories
  - [ ] Auto-generate filenames
  - [ ] Use pathvalidate for safety
- [ ] Add format support
  - [ ] Accept format parameter
  - [ ] Default to configured format
  - [ ] Save with appropriate extension
- [ ] Add token count configuration
  - [ ] Accept tokens parameter
  - [ ] Use default from config
  - [ ] Validate range
- [ ] Implement progress indication
  - [ ] Show current fetch
  - [ ] Display progress for multiple fetches
- [ ] Add error handling
  - [ ] API failures
  - [ ] File system errors
  - [ ] Invalid parameters
- [ ] Write integration tests

## Task 5: Testing & Documentation
- [ ] Set up pytest framework
- [ ] Create test fixtures for API responses
- [ ] Write unit tests for all modules
- [ ] Write integration tests for CLI commands
- [ ] Add test coverage reporting
- [ ] Update README with usage examples
- [ ] Add inline code documentation
- [ ] Create example configuration file

## Task 6: Security & Error Handling
- [ ] Implement API key masking in logs/output
- [ ] Add input validation for all user inputs
- [ ] Implement secure file path handling
- [ ] Add comprehensive error messages
- [ ] Implement retry logic for transient errors
- [ ] Add request timeout configuration
- [ ] Validate API responses before processing

## Acceptance Criteria
- [ ] All commands work as specified in README
- [ ] Proper error handling with user-friendly messages
- [ ] No sensitive data (API keys) in logs or output
- [ ] All file operations are safe (no path traversal)
- [ ] Tests pass with >80% coverage
- [ ] Code follows Python best practices
- [ ] Documentation is complete and accurate

## Development Notes
- Start with API client as it's the foundation
- Test each component thoroughly before moving to the next
- Use mock API responses for testing to avoid rate limits
- Consider adding debug mode for troubleshooting
- Keep security considerations in mind throughout