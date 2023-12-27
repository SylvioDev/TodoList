from django.db import models

# Category class 

class Category(models.Model):
    name = models.CharField(max_length = 55)
    
    def __str__(self):
        return self.name

# Todo class

class Todo(models.Model):
    title = models.CharField(max_length = 40)
    completed = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    category = models.ForeignKey(Category, 
                                on_delete = models.SET_NULL, 
                                blank = True, 
                                null = True)

    def __str__(self):
        return self.title
    