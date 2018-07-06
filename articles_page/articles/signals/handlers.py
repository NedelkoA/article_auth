def create_profile(sender, **kwargs):
    from django.contrib.auth.models import Group
    from .. import models
    user = kwargs['instance']
    if kwargs['created'] and not user.is_superuser:
        group = Group.objects.get(name='User group')
        group.user_set.add(user)
        models.UserProfile.objects.create(user=user)


def create_group(name, permissions):
    from django.contrib.auth.models import Group
    try:
        Group.objects.get(name=name)
    except Group.DoesNotExist:
        group = Group.objects.create(name=name)
        [group.permissions.add(permission) for permission in permissions]


def define_company_groups(sender, **kwargs):
    from django.contrib.auth.models import Permission
    permissions_user = [
        Permission.objects.get(codename='add_article'),
    ]
    permissions_staff = [
        Permission.objects.get(codename='change_article'),
        Permission.objects.get(codename='change_status'),
        Permission.objects.get(codename='add_category'),
    ]
    create_group('User group', permissions_user)
    create_group('Staff group', permissions_staff)
