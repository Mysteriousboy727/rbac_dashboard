from django.contrib.auth import get_user_model

User = get_user_model()

# Create Manager user
manager = User.objects.create_user(
    username='manager',
    email='manager@example.com',
    password='manager123',
    role='manager',
    first_name='Manager',
    last_name='User'
)

# Create Regular user
user = User.objects.create_user(
    username='user',
    email='user@example.com',
    password='user123',
    role='user',
    first_name='Regular',
    last_name='User'
)

print('✓ Users created successfully!')
print('Login credentials:')
print('  Admin: admin / admin123')
print('  Manager: manager / manager123')
print('  User: user / user123')