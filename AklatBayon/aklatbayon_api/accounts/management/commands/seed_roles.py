from django.core.management.base import BaseCommand
from accounts.models import Role, Permission

class Command(BaseCommand):
    help = 'Seeds initial roles and permissions exactly matching the original Laravel AklatBayon system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding permissions...')
        
        permissions_data = [
            # Books
            {'name': 'Issue Books', 'slug': 'can_issue_books', 'group': 'Books'},
            {'name': 'Return Books', 'slug': 'can_return_books', 'group': 'Books'},
            {'name': 'Manage Books', 'slug': 'can_manage_books', 'group': 'Books'},
            # Catalog
            {'name': 'Add / Manage Categories', 'slug': 'can_add_categories', 'group': 'Catalog'},
            {'name': 'Manage Authors', 'slug': 'can_manage_authors', 'group': 'Catalog'},
            {'name': 'Manage Publishers', 'slug': 'can_manage_publishers', 'group': 'Catalog'},
            # Reports
            {'name': 'View Reports', 'slug': 'can_view_reports', 'group': 'Reports'},
            # Users
            {'name': 'Manage Users', 'slug': 'can_manage_users', 'group': 'Users'},
            {'name': 'Manage Roles & Permissions', 'slug': 'can_manage_roles', 'group': 'Users'},
            {'name': 'Manage Students', 'slug': 'can_manage_students', 'group': 'Users'},
            # System
            {'name': 'Manage Settings', 'slug': 'can_manage_settings', 'group': 'System'},
            {'name': 'Manage Backups', 'slug': 'can_manage_backups', 'group': 'System'},
            {'name': 'View Audit Logs', 'slug': 'can_view_audit_logs', 'group': 'System'},
        ]

        perms = {}
        for pdata in permissions_data:
            perm, created = Permission.objects.get_or_create(
                slug=pdata['slug'],
                defaults={'name': pdata['name'], 'group': pdata['group']}
            )
            perms[pdata['slug']] = perm

        self.stdout.write('Seeding roles...')
        roles_data = [
            {'name': 'Administrator', 'slug': 'administrator', 'desc': 'Full system access — all permissions automatically granted'},
            {'name': 'Librarian', 'slug': 'librarian', 'desc': 'Circulation, catalog management, and reporting'},
            {'name': 'Student Assistant', 'slug': 'student_assistant', 'desc': 'Issue/Return books and basic circulation'},
            {'name': 'Student', 'slug': 'student', 'desc': 'Self-service portal — view catalog, borrowing history'},
            {'name': 'Faculty', 'slug': 'faculty', 'desc': 'Faculty portal — view catalog, extended borrowing'},
        ]

        roles = {}
        for rdata in roles_data:
            role, created = Role.objects.get_or_create(
                slug=rdata['slug'],
                defaults={'name': rdata['name'], 'description': rdata['desc']}
            )
            roles[rdata['slug']] = role

        self.stdout.write('Assigning permissions to roles...')
        
        # Assign Librarian Permissions
        librarian_perms = [
            'can_issue_books', 'can_return_books', 'can_manage_books',
            'can_add_categories', 'can_manage_authors', 'can_manage_publishers',
            'can_view_reports', 'can_manage_students'
        ]
        roles['librarian'].permissions.set([perms[slug] for slug in librarian_perms])
        
        # Assign Student Assistant Permissions
        student_asst_perms = ['can_issue_books', 'can_return_books']
        roles['student_assistant'].permissions.set([perms[slug] for slug in student_asst_perms])

        self.stdout.write(self.style.SUCCESS('Successfully seeded roles and permissions.'))
