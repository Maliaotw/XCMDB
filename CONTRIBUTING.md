# XCMDB - Contributor Guide

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- Docker & Docker Compose（可選，用於 vCenter/VMware 連線）

### Setup

1. Clone and install dependencies:
   ```bash
   git clone <repo-url>
   cd XCMDB
   pip install -r requirements.txt
   ```

2. Set up environment:
   ```bash
   cp backend/cmdb/.env.example backend/cmdb/.env
   # Edit .env with your DB and Redis settings
   ```

3. Run migrations:
   ```bash
   cd backend/cmdb
   python manage.py migrate
   ```

4. Start the server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
XCMDB/
├── backend/cmdb/           # Django backend
│   ├── cmdb/               # Django project settings
│   ├── apps/               # Business logic (CMDB)
│   ├── hosts/              # Host management
│   ├── vm/                 # VM management
│   ├── authentication/     # Auth & RBAC
│   └── ...
├── frontend/               # Vue.js frontend
└── docs/                   # Architecture docs
```

## Development Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature
   ```

2. Make changes and commit with clear messages:
   ```bash
   git commit -m "Add: VM sync with vCenter"
   ```

3. Push and create a Pull Request:
   ```bash
   git push origin feature/your-feature
   ```

## Code Style

- Use Black for Python formatting
- Follow PEP 8 for Python code
- Use camelCase for API fields, snake_case for Python code
- Write tests for new features

## Testing

Run tests with:
```bash
cd backend/cmdb
python manage.py test
```

## Submitting Changes

1. Ensure all tests pass
2. Update documentation if needed
3. Get at least one review
4. Squash commits and merge to main

## Reporting Issues

- Use the [issue tracker](https://github.com/anomalyco/opencode/issues)
- Include steps to reproduce
- Add logs and screenshots if possible
