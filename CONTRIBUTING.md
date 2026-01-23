# Contributing to NeuroLearn

Thank you for your interest in contributing to NeuroLearn! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Git

### Setting Up Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lightrunnerwastaken/robot-eye.git
   cd robot-eye
   ```

2. **Set up Backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   cp .env.example .env
   # Edit .env with your local settings
   ```

3. **Set up Frontend**
   ```bash
   cd frontend
   npm install
   ```

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest --cov=backend           # With coverage
pytest -k test_goals           # Run specific test file
pytest -m unit                 # Run tests with specific marker
```

### Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow-running tests

## 📝 Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use docstrings for public functions and classes
- Import order: standard library, third-party, local

**Example:**
```python
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter
from sqlalchemy.orm import Session

from backend.models import Goal


def create_goal(
    session: Session, 
    subject: str, 
    topic: str
) -> Goal:
    """
    Create a new learning goal.
    
    Args:
        session: Database session
        subject: Subject name
        topic: Topic name
        
    Returns:
        Created Goal object
    """
    goal = Goal(subject=subject, topic=topic)
    session.add(goal)
    session.commit()
    return goal
```

### TypeScript (Frontend)

- Use TypeScript strict mode
- Prefer functional components with hooks
- Use proper types (avoid `any`)
- Follow Airbnb style guide

## 🔧 Making Changes

### Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise commit messages
   - Add tests for new features
   - Update documentation as needed

3. **Run tests**
   ```bash
   # Backend
   pytest backend/tests/
   
   # Frontend (if applicable)
   npm test
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples:**
```
feat: add user authentication
fix: resolve CORS issue in API
docs: update API documentation
refactor: simplify goal creation logic
test: add unit tests for review service
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description** - Clear description of the issue
2. **Steps to Reproduce** - Detailed steps to reproduce the problem
3. **Expected Behavior** - What you expected to happen
4. **Actual Behavior** - What actually happened
5. **Environment** - OS, Python/Node version, browser (if applicable)
6. **Screenshots** - If applicable
7. **Error Messages** - Full error messages and stack traces

## 💡 Suggesting Features

Feature suggestions are welcome! Please:

1. Check if the feature has already been suggested
2. Clearly describe the feature and its benefits
3. Provide use cases and examples
4. Consider implementation complexity

## 📋 Pull Request Process

1. **Update documentation** - README, API docs, etc.
2. **Add tests** - Ensure adequate test coverage
3. **Run linters** - Ensure code passes all checks
4. **Update CHANGELOG** - If applicable
5. **Request review** - Tag relevant maintainers

### PR Checklist

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts
- [ ] PR description explains changes

## 🏗️ Architecture Guidelines

### Backend

- **Routes** - API endpoint definitions
- **Services** - Business logic
- **Models** - Database models (SQLAlchemy)
- **Schemas** - API schemas (Pydantic)
- **Dependencies** - Shared dependencies

### Frontend

- **Components** - Reusable UI components
- **Pages** - Next.js pages
- **Lib** - Utility functions and API clients
- **Styles** - Tailwind CSS

## 🔐 Security

- Never commit secrets, API keys, or passwords
- Use environment variables for configuration
- Validate all user input
- Follow OWASP security best practices
- Report security vulnerabilities privately

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📞 Getting Help

- Open an issue for bugs or questions
- Check existing issues and documentation
- Be respectful and patient

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to NeuroLearn! 🎉
