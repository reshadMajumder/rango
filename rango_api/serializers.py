#rango/serializers.py

from pydantic import BaseModel
from typing import List, Any, Optional

class ModelSerializer:
    """Simple serializer for Rango models."""
    
    def __init__(self, instance=None, data=None, many=False):
        self.instance = instance
        self.initial_data = data
        self.many = many
        self.validated_data = {}
        self.errors = {}

    @property
    def data(self):
        if self.instance is None:
            return None
        if self.many:
            return [self._serialize(obj) for obj in self.instance]
        return self._serialize(self.instance)

    def is_valid(self):
        if not self.initial_data:
            self.errors = {"detail": "No data provided"}
            return False
        self.validated_data = self.initial_data
        return True

    def _serialize(self, obj):
        # Get fields from the Meta class if it exists
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'fields'):
            fields = self.Meta.fields
        else:
            # Fallback to all model fields
            fields = [field for field in dir(obj) if not field.startswith('_') and not callable(getattr(obj, field))]
        
        result = {}
        for field in fields:
            if hasattr(obj, field):
                value = getattr(obj, field)
                # Handle datetime objects
                if hasattr(value, 'isoformat'):
                    result[field] = value.isoformat()
                else:
                    result[field] = value
        return result
