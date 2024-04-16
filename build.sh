#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate


# Hardcoded values for superuser
username="admin"
email="admin@example.com"
password="hardcodedpassword123"

# Django's manage.py path
manage_py_path="/path/to/your/django/project/manage.py"

# Create Django superuser
echo "Creating Django superuser..."
python $manage_py_path createsuperuser --username $username --email $email --noinput

# Set password for the created superuser
echo "Setting password for the superuser..."
echo "$password
$password
" | python $manage_py_path changepassword $username

# Check if superuser creation was successful
if [ $? -eq 0 ]; then
    echo "Superuser created successfully."
else
    echo "Error creating superuser. Please check the inputs and try again."
fi
