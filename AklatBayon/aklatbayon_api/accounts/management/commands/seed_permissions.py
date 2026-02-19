from django.core.management.base import BaseCommand
from accounts.models import Permission, Role


PERMISSIONS = [
    # Users
    ('can_view_users', 'View Users', 'users'),
    ('can_create_users', 'Create Users', 'users'),
    ('can_edit_users', 'Edit Users', 'users'),
    ('can_delete_users', 'Delete Users', 'users'),
    # Roles
    ('can_manage_roles', 'Manage Roles & Permissions', 'roles'),
    # Books
    ('can_view_books', 'View Books', 'books'),
    ('can_create_books', 'Create Books', 'books'),
    ('can_edit_books', 'Edit Books', 'books'),
    ('can_delete_books', 'Delete Books', 'books'),
    # Authors
    ('can_manage_authors', 'Manage Authors', 'books'),
    # Publishers
    ('can_manage_publishers', 'Manage Publishers', 'books'),
    # Categories
    ('can_manage_categories', 'Manage Categories', 'books'),
    # Students
    ('can_view_students', 'View Students', 'students'),
    ('can_create_students', 'Create Students', 'students'),
    ('can_edit_students', 'Edit Students', 'students'),
    ('can_delete_students', 'Delete Students', 'students'),
    # Circulation
    ('can_issue_books', 'Issue Books', 'circulation'),
    ('can_return_books', 'Return Books', 'circulation'),
    ('can_view_transactions', 'View Transactions', 'circulation'),
    # Fines
    ('can_view_fines', 'View Fines', 'fines'),
    ('can_collect_fines', 'Collect Fines', 'fines'),
    ('can_waive_fines', 'Waive Fines', 'fines'),
    # Reports
    ('can_view_reports', 'View Reports', 'reports'),
    # Inventory
    ('can_view_inventory', 'View Inventory', 'inventory'),
    # Settings
    ('can_manage_settings', 'Manage Settings', 'system'),
    # Backup
    ('can_manage_backup', 'Manage Backup & Restore', 'system'),
    # Audit Logs
    ('can_view_audit_logs', 'View Audit Logs', 'system'),
]

ROLES = {
    'librarian': {
        'name': 'Librarian',
        'description': 'Full access to all library functions',
        'permissions': '__all__',  # Gets all permissions
    },
    'student_assistant': {
        'name': 'Student Assistant',
        'description': 'Can manage circulation and view records',
        'permissions': [
            'can_view_books', 'can_view_students', 'can_view_transactions',
            'can_issue_books', 'can_return_books', 'can_view_fines',
            'can_collect_fines', 'can_view_inventory',
        ],
    },
    'student': {
        'name': 'Student',
        'description': 'Can view catalog only',
        'permissions': ['can_view_books'],
    },
    'faculty': {
        'name': 'Faculty',
        'description': 'Can view catalog and borrow books',
        'permissions': ['can_view_books', 'can_view_transactions'],
    },
}


class Command(BaseCommand):
    help = 'Seed initial permissions and roles'

    def handle(self, *args, **options):
        self.stdout.write('Seeding permissions...')
        perm_objects = {}
        for slug, name, group in PERMISSIONS:
            perm, created = Permission.objects.get_or_create(
                slug=slug, defaults={'name': name, 'group': group}
            )
            perm_objects[slug] = perm
            if created:
                self.stdout.write(f'  + {name}')

        self.stdout.write(f'\nSeeding roles...')
        all_perms = list(perm_objects.values())

        for slug, config in ROLES.items():
            role, created = Role.objects.get_or_create(
                slug=slug,
                defaults={'name': config['name'], 'description': config['description']}
            )
            if config['permissions'] == '__all__':
                role.permissions.set(all_perms)
            else:
                role.permissions.set([perm_objects[p] for p in config['permissions']])

            status = 'Created' if created else 'Updated'
            self.stdout.write(f'  {status}: {config["name"]} ({role.permissions.count()} permissions)')

        self.stdout.write(self.style.SUCCESS('\n✅ Seeding complete!'))
