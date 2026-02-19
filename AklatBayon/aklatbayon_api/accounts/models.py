from django.contrib.auth.models import AbstractUser
from django.db import models


class Permission(models.Model):
    """Granular permission (e.g. can_manage_users, can_issue_books)."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    group = models.CharField(max_length=50, help_text="Logical group, e.g. 'users', 'books'")

    class Meta:
        ordering = ['group', 'name']

    def __str__(self):
        return self.name


class Role(models.Model):
    """Role that bundles permissions (e.g. Librarian, Student)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Custom user with user_type and role."""
    class UserType(models.TextChoices):
        LIBRARIAN = 'librarian', 'Librarian'
        STUDENT_ASSISTANT = 'student_assistant', 'Student Assistant'
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'
        NON_TEACHER = 'non_teacher', 'Non-Teacher'
        STAFF = 'staff', 'Staff'

    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.STUDENT)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"

    def has_perm_slug(self, perm_slug):
        """Check if user's role has a specific permission."""
        if self.is_superuser:
            return True
        if self.role is None:
            return False
        return self.role.permissions.filter(slug=perm_slug).exists()
