# Rango API Framework

A modern Python web framework built on Starlette with Django-like features for rapid API development.

## Features

- **Starlette Integration**: Built on top of Starlette for high performance and ASGI compatibility
- **Django-like Structure**: Familiar project and app structure similar to Django
- **ORM Integration**: Built-in Tortoise ORM support with Aerich migrations
- **Generic Views**: Pre-built views for common CRUD operations
- **Serializers**: Django REST Framework-like serializers
- **CLI Tools**: Command-line interface for project management
- **CORS Middleware**: Built-in CORS support
- **Manual Database Management**: Safe, Django-like database migration workflow

## Installation

### Option 1: Install globally (recommended for CLI usage)
```bash
pip install rango-api
```

### Option 2: Use manage.py (for project-specific usage)
```bash
# Clone or download the framework
# Use python manage.py commands instead of rango commands
```

## Quick Start

### Option A: Using global CLI (if installed globally)

```bash
# 1. Create a new project
rango startproject myproject
cd myproject

# 2. Create an app
rango startapp blog

# 3. Initialize database
rango initdb

# 4. Start server
rango runserver
```

### Option B: Using manage.py (project-specific)

```bash
# 1. Create a new project
python manage.py startproject myproject
cd myproject

# 2. Create an app
python manage.py startapp blog

# 3. Initialize database
python manage.py initdb

# 4. Start server
python manage.py runserver
```

## Database Management

Rango Framework uses Tortoise ORM with Aerich for database migrations, providing a Django-like experience.

### Initial Setup (First Time Only)

```bash
# After creating a project and app
python manage.py initdb
```

### Development Workflow

```bash
# 1. Modify models in your app
# ... edit models.py ...

# 2. Create migrations
python manage.py makemigrations "description of changes"

# 3. Apply migrations
python manage.py migrate

# 4. Check status (optional)
python manage.py migrate_status
```

### Production Safety

- **No automatic migrations**: Database schema changes must be explicitly applied
- **Manual migration control**: You control when and how migrations are applied
- **Automatic DB connection**: Database connection is initialized on first request
- **Migration tracking**: Aerich tracks applied migrations
- **Rollback support**: Aerich supports migration rollbacks

For detailed database management guide, see [DATABASE_GUIDE.md](DATABASE_GUIDE.md).

## Tutorial

### Create models with ForeignKey

```python
from tortoise import fields, models

class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

class Product(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    category = fields.ForeignKeyField('models.Category', related_name='products')
```

### Serializers (nested FK supported)

```python
from rango_api.serializers import ModelSerializer
from .models import Category, Product

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "category"]  # can send category or category_id
        nested_serializers = {
            'Category': CategorySerializer
        }
```

### Views (generic, with FK optimization)

```python
from rango_api.generics import ListCreateView, RetrieveUpdateDeleteView
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(ListCreateView):
    model = Product
    serializer_class = ProductSerializer
    select_related = ['category']  # optimize FK

class ProductDetailView(RetrieveUpdateDeleteView):
    model = Product
    serializer_class = ProductSerializer
    select_related = ['category']
```

### URLs

```python
from rango_api.router import Router
from .views import ProductListCreateView, ProductDetailView

router = Router()
router.add("/products", ProductListCreateView, methods=["GET", "POST"])
router.add("/products/{id}", ProductDetailView, methods=["GET", "PUT", "PATCH", "DELETE"])
```

### Test the API

- Create category:
```bash
curl -X POST http://127.0.0.1:8000/categories \
  -H "Content-Type: application/json" \
  -d '{"name":"Electronics"}'
```

- Create product (supports category or category_id):
```bash
curl -X POST http://127.0.0.1:8000/products \
  -H "Content-Type: application/json" \
  -d '{"title":"Phone","category":1}'
```

## Extensibility (DRF-like Hooks)

You can override hooks in generic views to customize behavior:

```python
class ProductListCreateView(ListCreateView):
    model = Product
    serializer_class = ProductSerializer

    def get_queryset(self, request):
        return self.model.all().select_related('category')

    async def before_create(self, request, data: dict) -> dict:
        # mutate/validate incoming data
        data.setdefault("title", data.get("title", "Untitled"))
        return data

    async def after_create(self, request, obj):
        # side-effects, logging, etc.
        return obj

class ProductDetailView(RetrieveUpdateDeleteView):
    model = Product
    serializer_class = ProductSerializer

    async def before_update(self, request, obj, data: dict) -> dict:
        # e.g. normalize FK input
        if 'category' in data and 'category_id' not in data:
            data['category_id'] = data.pop('category')
        return data
```

Available hooks include: `get_queryset`, `filter_queryset`, `before_create`, `perform_create`, `after_create`, `before_update`, `perform_update`, `after_update`, `before_delete`, `perform_delete`, `after_delete`.

## Project Structure

```
myproject/
├── apps/
│   └── blog/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── asgi.py
├── main.py
└── manage.py
```

## Basic Usage

### Models

```python
from tortoise import fields, models

class Post(models.Model):
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
```

### Serializers

```python
from rango_api.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "created_at"]
```

### Views

```python
from rango_api.generics import ListCreateView, RetrieveUpdateDeleteView
from .models import Post
from .serializers import PostSerializer

class PostListCreateView(ListCreateView):
    model = Post
    serializer_class = PostSerializer

class PostDetailView(RetrieveUpdateDeleteView):
    model = Post
    serializer_class = PostSerializer
```

### URLs

```python
from rango_api.router import Router
from .views import PostListCreateView, PostDetailView

router = Router()
router.add("/posts", PostListCreateView, methods=["GET", "POST"])
router.add("/posts/{id}", PostDetailView, methods=["GET", "PUT", "DELETE"])
```

## CLI Commands

### Project Management
- `python manage.py startproject <name>` - Create a new project
- `python manage.py startapp <name>` - Create a new app
- `python manage.py runserver [host] [port]` - Start development server

### Database Management
- `python manage.py initdb` - Initialize database and Aerich config (first time only)
- `python manage.py makemigrations [message]` - Create database migrations
- `python manage.py migrate` - Apply database migrations
- `python manage.py migrate_status` - Show migration status

### Alternative CLI (if installed globally)
- `rango startproject <name>` - Create a new project
- `rango startapp <name>` - Create a new app
- `rango initdb` - Initialize database
- `rango makemigrations [message]` - Create migrations
- `rango migrate` - Apply migrations
- `rango migrate_status` - Show migration status
- `rango runserver [host] [port]` - Start development server

## Requirements

- Python 3.8+
- Starlette
- Tortoise ORM
- Aerich (for migrations)
- Uvicorn

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you have any questions or need help, please open an issue on GitHub.