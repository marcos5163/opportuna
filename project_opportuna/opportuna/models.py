import uuid
from django.db import models
from typing import Any


class AllManager(models.Manager):
    def get_queryset(self):
        return super(AllManager, self).get_queryset().filter(is_deleted=False)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AllManager()
    admin_manager = models.Manager()

    class Meta:
        abstract = True

    def add_to_jsonfield(self, field_name: str, key: str, value: Any) -> None:
        """
        Adds a key, value to provided json field.
        Overwrites existing value if it exists.
        Note: does not call .save() on the instance
        """

        jsonfield_data = getattr(self, field_name) or {}
        jsonfield_data[key] = value
        setattr(self, field_name, jsonfield_data)

    def remove_from_jsonfield(self, field_name: str, key: str) -> None:
        """
        Removes a key from provided json field.
        Note: does not call .save() on the instance
        """

        jsonfield_data = getattr(self, field_name) or {}
        if key in jsonfield_data:
            jsonfield_data.pop(key)
        setattr(self, field_name, jsonfield_data)

    def get_from_jsonfield(self, field_name: str, key: str, default=None):
        """
        Fetches a key from provided json field.
        Returns default is not found.
        """

        jsonfield_data = getattr(self, field_name) or {}
        return jsonfield_data.get(key, default)
    

class Post(BaseModel):
    title = models.CharField(max_length=500) 
    discription = models.TextField()
    company = models.CharField(max_length=100)
    meta_tags = models.JSONField(default={})
       
