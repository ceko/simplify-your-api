from django.contrib.auth.models import User
client, created = User.objects.get_or_create(
    username='client',
    email='email@clientcompany.com'
)
client.set_password('midichlorians')
client.save()

su, created = User.objects.get_or_create(
    username='su',
    email='su@clientcompany.com'
)
su.is_staff = True
su.is_superuser = True
su.set_password('god')
su.save()

from rest_framework.authtoken.models import Token
token, created = Token.objects.get_or_create(user=client)

print("Session Login - client:midichlorians")
print("Token Login - {}".format(token.key))