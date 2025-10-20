# Rango Framework - Database Management Guide

## Overview
Rango Framework uses Tortoise ORM with Aerich for database migrations, providing a Django-like experience for database management.

## Database Workflow

### 1. Initial Setup (First Time Only)

After creating a new project, you need to initialize the database:

```bash
# Initialize Aerich configuration
python manage.py initdb
```

This command will:
- Initialize Aerich configuration (`aerich init -t project.settings.TORTOISE_ORM`)
- Create the initial database (`aerich init-db`)
- Set up the migration system

### 2. Development Workflow

#### When you create or modify models:

```bash
# Create migration files
python manage.py makemigrations "description of changes"

# Apply migrations to database
python manage.py migrate
```

#### Check migration status:
```bash
python manage.py migrate_status
```

### 3. Production Safety

The framework is designed to be production-safe:

- **No automatic migrations**: Database schema changes must be explicitly applied
- **Manual migration control**: You control when and how migrations are applied
- **Automatic DB connection**: Database connection is initialized on first request
- **Migration tracking**: Aerich tracks applied migrations
- **Rollback support**: Aerich supports migration rollbacks

### 4. Available Commands

| Command | Description | Django Equivalent |
|---------|-------------|-------------------|
| `initdb` | Initialize database and Aerich config | `migrate` (first time) |
| `makemigrations` | Create migration files | `makemigrations` |
| `migrate` | Apply migrations | `migrate` |
| `migrate_status` | Show migration status | `showmigrations` |

### 5. Example Workflow

```bash
# 1. Create a new project
python manage.py startproject myproject
cd myproject

# 2. Create an app
python manage.py startapp blog

# 3. Initialize database (first time only)
python manage.py initdb

# 4. Modify models in apps/blog/models.py
# ... make changes to models ...

# 5. Create migrations
python manage.py makemigrations "add blog models"

# 6. Apply migrations
python manage.py migrate

# 7. Start development server
python manage.py runserver
```

### 6. Advanced Aerich Commands

For advanced database operations, you can use Aerich directly:

```bash
# Show migration history
aerich history

# Rollback to a specific migration
aerich downgrade <migration_name>

# Show current migration status
aerich status

# Create migration without applying
aerich migrate --name "migration_name"

# Apply specific migration
aerich upgrade <migration_name>
```

### 7. Best Practices

1. **Always create migrations** after model changes
2. **Test migrations** in development before production
3. **Backup database** before applying migrations in production
4. **Use descriptive migration names** for better tracking
5. **Review migration files** before applying them

### 8. Troubleshooting

#### Database not initialized error:
```bash
python manage.py initdb
```

#### Migration conflicts:
```bash
# Check status
python manage.py migrate_status

# Resolve conflicts manually
aerich status
```

#### Reset database (development only):
```bash
# Delete database file
rm db.sqlite3

# Reinitialize
python manage.py initdb
```

## Security Notes

- **Production**: Never run `initdb` in production
- **Backups**: Always backup before migrations in production
- **Testing**: Test migrations in staging environment first
- **Rollback**: Keep rollback plan ready for production migrations
