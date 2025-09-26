# Contributing to Rising Topics

Thank you for your interest in contributing to Rising Topics! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Git

### Development Setup

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/rising-topics.git
   cd rising-topics
   ```

3. **Install dependencies**
   ```bash
   # Frontend dependencies
   npm install
   
   # Python dependencies
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Run tests**
   ```bash
   # Run all tests
   npm test
   
   # Run MVP tests only
   npm run test:mvp
   
   # Run specific test
   python tests/test_mvp_functionality.py
   ```

## 📝 Making Changes

### 1. Create a Feature Branch
```bash
git checkout -b feature/amazing-feature
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes
- Write clean, readable code
- Follow TypeScript best practices
- Add tests for new features
- Update documentation as needed

### 3. Test Your Changes
```bash
# Run linting
npm run lint

# Fix linting issues
npm run lint:fix

# Run type checking
npm run type-check

# Run tests
npm test

# Build the application
npm run build
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add amazing feature"
# or
git commit -m "fix: resolve bug in data processing"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/amazing-feature
# Then create a PR on GitHub
```

## 🎯 Code Style Guidelines

### TypeScript/React
- Use TypeScript for all new code
- Follow the existing ESLint configuration
- Use functional components with hooks
- Prefer `const` over `let` when possible
- Use meaningful variable and function names

### Python
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused

### Git Commit Messages
We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting changes
refactor: code refactoring
test: add or update tests
chore: maintenance tasks
```

## 🧪 Testing

### Frontend Tests
- Unit tests for components and hooks
- Integration tests for data flow
- End-to-end tests for critical user journeys

### Backend Tests
- Unit tests for data processing functions
- Integration tests for the data pipeline
- Error handling tests

### Running Tests
```bash
# All tests
npm test

# Frontend tests only
npm run test:frontend

# Backend tests only
npm run test:backend

# MVP functionality tests
npm run test:mvp
```

## 📚 Documentation

### Code Documentation
- Use JSDoc for TypeScript functions
- Use docstrings for Python functions
- Add comments for complex logic
- Keep README files updated

### API Documentation
- Document all API endpoints
- Include request/response examples
- Document error codes and messages

## 🐛 Reporting Issues

### Bug Reports
When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, browser, Node.js version)

### Feature Requests
For feature requests, please include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if you have ideas)
- Any relevant examples or references

## 🔒 Security

### Reporting Security Issues
- **DO NOT** create public issues for security vulnerabilities
- Email security issues to: security@risingtopics.com
- Include detailed information about the vulnerability
- We'll respond within 48 hours

### Security Best Practices
- Never commit secrets or API keys
- Use environment variables for sensitive data
- Keep dependencies updated
- Run security audits regularly: `npm run security`

## 🏗️ Project Structure

```
rising-topics/
├── src/app/              # Next.js frontend
│   ├── components/       # React components
│   ├── hooks/           # Custom React hooks
│   ├── services/        # Data services
│   └── types.ts         # TypeScript types
├── scripts/             # Python data pipeline
├── tests/               # Test suite
├── public/data/         # Generated data files
└── docs/               # Documentation
```

## 🤝 Code Review Process

### For Contributors
1. Ensure all tests pass
2. Update documentation if needed
3. Request review from maintainers
4. Address feedback promptly
5. Keep PRs focused and small

### For Reviewers
1. Check code quality and style
2. Verify tests are adequate
3. Test the changes locally
4. Provide constructive feedback
5. Approve when ready

## 📞 Getting Help

- **Documentation**: Check the README and docs folder
- **Issues**: Search existing issues first
- **Discussions**: Use GitHub Discussions for questions
- **Email**: contact@risingtopics.com

## 🎉 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to Rising Topics! 🚀
