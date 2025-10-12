from tortoise import fields, models





class Student(models.Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    age = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
