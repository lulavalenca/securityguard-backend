# Contributing Guidelines

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Write/update tests
5. Ensure all tests pass
6. Commit with clear messages
7. Push to your fork
8. Create Pull Request

## Code Style

### Python

- Use Black for formatting
- Follow PEP 8
- Max line length: 100 chars
- Type hints where applicable

### Commits

```
feat: Add new threat detection algorithm
fix: Resolve database migration issue
docs: Update API documentation
test: Add unit tests for SSL validation
refactor: Improve error handling
perf: Optimize database queries
```

## Pull Request Process

1. Update README.md with changes
2. Add tests for new functionality
3. Ensure CI/CD pipeline passes
4. Request review from maintainers
5. Address review comments
6. Maintain PR up to date with main branch

## Testing Requirements

- Minimum 80% code coverage
- All new features must have tests
- Integration tests for API endpoints
- Unit tests for services

```bash
pytest app/tests -v --cov=app --cov-report=term-missing
```

## Documentation

- Update docstrings for functions
- Add comments for complex logic
- Update API documentation
- Include examples for new endpoints

## Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Security considerations addressed
- [ ] Performance impact analyzed

## Reporting Issues

Use GitHub Issues with:

1. Clear title
2. Detailed description
3. Steps to reproduce
4. Expected vs actual behavior
5. Environment details
6. Relevant logs/screenshots

## Feature Requests

Describe:

1. Problem being solved
2. Proposed solution
3. Alternative approaches
4. Potential impact

## Code of Conduct

Be respectful, inclusive, and professional. See CODE_OF_CONDUCT.md
