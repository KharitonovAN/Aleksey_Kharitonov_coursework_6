from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        moderator_group, created = Group.objects.get_or_create(name='Moderator')
        if created:
            permissions = Permission.objects.filter(
                codename__in=['view_mailingsettings', 'change_mailingsettings',
                              'set_active', 'view_user', 'set_active']
            )
            moderator_group.permissions.set(permissions)

        blogpost_manager_group, created = Group.objects.get_or_create(name='BlogPostManager')
        if created:
            permissions = Permission.objects.filter(
                codename__in=['add_blogpost', 'view_blogpost', 'change_blogpost', 'delete_blogpost']
            )
            blogpost_manager_group.permissions.set(permissions)
