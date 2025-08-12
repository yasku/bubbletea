import streamlit_authenticator as stauth
import yaml
import os

# Define the path for the config file relative to the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config.yaml')

# --- User Data ---
# Passwords will be hashed, these are the plain-text versions
passwords_to_hash = ['admin123', 'operador123']

# Correct usage deduced from error messages:
# Hasher() with no args, then .generate() with passwords.
# This is the only syntax consistent with both previous errors.
hashed_passwords = stauth.Hasher(passwords_to_hash).generate()


# --- Create Config Structure ---
config = {
    'credentials': {
        'usernames': {
            'agustin_admin': {
                'email': 'admin@cambiototal.com',
                'name': 'Agustín (Admin)',
                'password': hashed_passwords[0]
            },
            'juan_operador': {
                'email': 'operador@cambiototal.com',
                'name': 'Juan (Operador)',
                'password': hashed_passwords[1]
            }
        }
    },
    'cookie': {
        'name': 'cambiototal_cookie',
        'key': 'unaclavesecretamuysegura', # This should be replaced with a real secret key
        'expiry_days': 30
    },
    'preauthorized': {
        'emails': [
            'admin@cambiototal.com'
        ]
    }
}

# --- Write Config to YAML File ---
try:
    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False)
    print(f"Authentication config file created successfully at: {CONFIG_PATH}")
except Exception as e:
    print(f"Error creating config file: {e}")
