from django.contrib.auth.models import Group


def my_handler(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        group = Group.objects.get(name='User group')
        group.user_set.add(user)
