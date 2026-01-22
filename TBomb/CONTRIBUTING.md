# Contributing to TBomb Enhanced

## Welcome Contributors! 🎉

Thank you for your interest in contributing to TBomb Enhanced. This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a welcoming environment
- Use this tool responsibly and ethically

## Getting Started

### 1. Fork and Clone
```bash
git clone https://github.com/yourusername/TBomb.git
cd TBomb
```

### 2. Set Up Development Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-async.txt -r requirements-dev.txt
```

### 3. Install Pre-commit Hooks
```bash
pre-commit install
```

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write clean, readable code
- Follow existing code style
- Add tests for new functionality
- Update documentation

### 3. Run Tests
```bash
pytest
black .
flake8 .
mypy .
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add new feature description"
```

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

## Contribution Types

### 🐛 Bug Fixes
- Fix existing issues
- Add regression tests
- Update documentation if needed

### ✨ New Features
- Add new API endpoints
- Implement new countries
- Enhance existing functionality

### 📚 Documentation
- Improve API documentation
- Add usage examples
- Fix typos and clarity

### 🧪 Testing
- Add unit tests
- Improve test coverage
- Add integration tests

### 🔧 Infrastructure
- CI/CD improvements
- Docker enhancements
- Performance optimizations

## Code Standards

### Python Style
- Follow PEP 8
- Use Black for formatting
- Maximum line length: 88 characters
- Use type hints

### Commit Messages
Follow conventional commits:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation
- `test:` testing
- `refactor:` code refactoring
- `perf:` performance improvements

### Testing Requirements
- All new code must have tests
- Maintain >80% test coverage
- Tests must pass on Python 3.8+

## Adding New API Endpoints

### 1. Research API
- Find legitimate APIs that send OTP/verification
- Test manually first
- Document rate limits

### 2. Add to Database
```python
# Add to apidata.json
{
  "name": "service_name",
  "method": "POST",
  "url": "https://api.service.com/verify",
  "data": {
    "phone": "{cc}{target}"
  },
  "identifier": "success"
}
```

### 3. Test Integration
```bash
python3 bomber_async.py --sms
# Test with your own number
```

### 4. Add Tests
```python
def test_new_api_endpoint():
    # Test API configuration
    # Test health checking
    pass
```

## Adding New Countries

### 1. Research Country
- Phone number format
- Popular services
- Regulatory considerations

### 2. Add Country Code
```python
# Add to isdcodes.json
"XX": {
  "name": "Country Name",
  "code": "XX"
}
```

### 3. Add APIs
```json
// Add to apidata.json under "sms"/"call"/"mail"
"XX": [
  {
    "name": "local_service",
    "method": "POST",
    "url": "https://local.service.com/api",
    "data": {"mobile": "{target}"},
    "identifier": "sent"
  }
]
```

## Review Process

### PR Requirements
- [ ] Tests pass
- [ ] Code coverage maintained
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Follows code standards

### Review Criteria
- Code quality and readability
- Test coverage and quality
- Documentation completeness
- Security considerations
- Performance impact

## Security Guidelines

### Do Not Include
- Real phone numbers in tests
- API keys or secrets
- Personal information
- Malicious code

### Do Include
- Input validation
- Rate limiting
- Error handling
- Security tests

## Performance Guidelines

- Use async/await for I/O operations
- Implement proper connection pooling
- Add timeout handling
- Monitor memory usage
- Profile performance-critical code

## Documentation Guidelines

- Update API.md for new features
- Add docstrings to all functions
- Include usage examples
- Keep README current

## Getting Help

- Open an issue for questions
- Join discussions in PRs
- Check existing documentation
- Review similar implementations

## Recognition

Contributors will be:
- Added to README contributors list
- Mentioned in release notes
- Credited in commit messages

## Ethical Usage

This tool is for:
- Educational purposes
- Testing your own systems
- Authorized security testing
- Research with proper permissions

This tool is NOT for:
- Harassment or spam
- Unauthorized testing
- Malicious activities
- Violating terms of service

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to TBomb Enhanced! 🚀