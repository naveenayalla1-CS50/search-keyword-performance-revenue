# Contributing Guidelines

Thank you for interest in contributing to the Search Keyword Performance Revenue Pipeline project. This document outlines the process for contributing code, reporting bugs, and improving documentation.

## Code of Conduct

- Be respectful and professional in all interactions
- Focus on constructive feedback
- Assume good intent from contributors
- Report any violations to the maintainers

## Getting Started

### Prerequisites
- Python 3.8+
- PySpark 3.1.0+
- Git
- pytest

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/search-keyword-performance.git
cd search-keyword-performance

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov  # Additional dev dependencies
```

## Contribution Process

### 1. Report a Bug

**Before submitting:**
- Check existing issues to avoid duplicates
- Gather relevant information (Python version, PySpark version, input data sample)
- Note error messages and stack traces

**Submit issue with:**
```
Title: [BUG] Clear description of the bug

Description:
- What behavior did you expect?
- What behavior did you observe?
- Steps to reproduce
- Code snippet if applicable

Environment:
- Python version: 
- PySpark version:
- OS:
```

### 2. Propose a Feature

**Submit issue with:**
```
Title: [FEATURE] Clear description of feature request

Description:
- What problem does this solve?
- Proposed solution
- Why is this valuable?
- Code examples or pseudocode

Alternatives:
- Have you considered other approaches?
```

### 3. Submit Code Changes

#### Step 1: Create a Branch
```bash
git checkout -b feature/keyword-extraction-improvements
# or
git checkout -b fix/revenue-parsing-bug
```

#### Step 2: Make Changes
- Keep commits focused (one logical change per commit)
- Write clear commit messages:
  ```
  Add support for Google Shopping referrer keywords
  
  - Extract product-specific search terms from shopping referrer format
  - Add 'ps_kw' parameter mapping for Google Shopping
  - Add unit tests for new extraction logic
  ```

#### Step 3: Write Tests
Every code change must include tests:

```python
# tests/test_extractors.py

def test_extract_google_shopping_keyword():
    """Test extraction from Google Shopping referrer."""
    referrer = "https://shopping.google.com/shopping?q=gaming+laptop"
    assert extract_search_keyword(referrer) == "gaming laptop"

def test_extract_revenue_with_decimal_places():
    """Test revenue extraction with various decimal precisions."""
    assert extract_revenue_from_product_list(
        "A;cat;1;99.999"
    ) == 99.999
```

Run tests locally:
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=extractors --cov=transformations
```

Aim for >80% code coverage on new code.

#### Step 4: Update Documentation
- Update README.md if you change functionality
- Add docstrings to all new functions
- Update EXAMPLES.md for new features

Example docstring format:
```python
def my_new_function(param1: str) -> Optional[float]:
    """
    Brief one-line description.
    
    Longer explanation if needed, including:
    - Algorithm details
    - Performance characteristics
    - Edge cases handled
    
    Args:
        param1: Description of param
    
    Returns:
        Optional[float]: Description of return value
    
    Raises:
        ValueError: If param1 is invalid
    
    Examples:
        >>> my_new_function("test")
        123.45
    """
```

#### Step 5: Commit and Push
```bash
git add .
git commit -m "Add support for Google Shopping referrer keywords"
git push origin feature/keyword-extraction-improvements
```

#### Step 6: Create Pull Request
- Reference related issues: "Fixes #123"
- Describe changes clearly
- Include before/after performance metrics if relevant
- Link to relevant documentation

**PR Template:**
```markdown
## Description
Brief summary of changes

## Fixes
- Fixes #123

## Changes Made
- Change 1
- Change 2

## Testing
- [x] Added unit tests
- [x] Ran pytest with coverage
- [x] Tested with sample data

## Performance Impact
- Processing time: No change
- Memory usage: +5MB per worker node

## Checklist
- [x] Code follows style guidelines
- [x] Added/updated tests
- [x] Updated documentation
- [x] All tests pass locally
```

## Code Standards

### Style Guide
- Follow PEP 8 for Python code
- Use 4 spaces for indentation (not tabs)
- Max line length: 100 characters
- Use meaningful variable names

### Type Hints
All functions must have type hints:
```python
# Good
def extract_domain(url: str) -> Optional[str]:
    ...

# Bad
def extract_domain(url):
    ...
```

### Error Handling
Use specific exception handling:
```python
# Good
try:
    result = float(value)
except ValueError:
    logger.error(f"Invalid float value: {value}")
    return 0.0

# Bad
try:
    result = float(value)
except:
    pass
```

### Comments
```python
# Good: Explains WHY, not WHAT
# We whitelist search engines to prevent poisoning with non-search referrers
known_domains = {"google.com", "bing.com"}

# Bad: States the obvious
# Check if domain is in known domains
if domain in known_domains:
```

### Testing Standards
- Write tests that verify behavior, not implementation
- Use descriptive test names
- Test edge cases and error conditions
- Aim for >80% coverage

```python
# Good
def test_extract_keyword_handles_url_encoded_spaces():
    """Verify spaces are decoded from + encoding."""
    assert extract_keyword("...?q=hello+world") == "hello world"

# Bad
def test1():
    assert extract_keyword("...?q=hello+world") == "hello world"
```

## Performance Guidelines

### When Adding Features
Benchmark before/after:
```bash
# Time processing on 10M record sample
time python app.py --INPUT_PATH sample_10m.tsv --OUTPUT_PATH output/
```

### Optimization Priorities
1. Correctness (always first)
2. Maintainability (clear code > clever code)
3. Performance (optimize only if bottleneck)

Optimization must not sacrifice clarity:
```python
# Good: Clear intent, acceptable performance
for product in product_list.split(","):
    revenue += extract_revenue(product)

# Bad: Premature optimization, harder to read/maintain
total = sum(float(p.split(";")[3]) for p in product_list.split(",") if len(p.split(";")) > 3)
```

## Release Process

### Versioning
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Creating a Release
```bash
# Update version in setup.py
# Update CHANGELOG.md
git tag -a v1.2.0 -m "Release v1.2.0: Add Google Shopping support"
git push origin v1.2.0
```

## Review Process

### For Maintainers
- Verify tests pass
- Check code quality and style
- Verify documentation is updated
- Ensure performance is acceptable
- Provide constructive feedback

### Timeline
- Simple changes (docs, tests): 1-2 days
- Feature additions: 3-5 days
- Breaking changes: 1+ weeks (discussion period)

## Common Issues

### Issue: "My changes cause tests to fail"

Solution:
```bash
# Run tests locally to catch issues early
pytest tests/ -v --tb=short

# Fix any failing tests before pushing
# Ensure you added tests for your new code
```

### Issue: "My PR has merge conflicts"

Solution:
```bash
# Sync with main
git fetch origin
git rebase origin/main

# Resolve conflicts, then
git add .
git rebase --continue
```

### Issue: "Code review feedback on my PR"

- Reply to each comment
- Make requested changes
- Push updates (don't force push unless instructed)
- Comment "Ready for re-review" when done

## Getting Help

- **Questions about contributing?** Open a discussion
- **Need help with your PR?** Ask in the PR comments
- **Found a bug?** Open an issue with reproduction steps
- **Have ideas?** Start a discussion before creating feature PR

## Acknowledgments

All contributors will be:
- Added to CONTRIBUTORS.md
- Recognized in release notes
- Given appropriate credit

Thank you for making this project better!

---

**Questions?** Contact the maintainers or open a discussion in the GitHub Issues section.
