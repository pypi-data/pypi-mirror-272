import os
import click


def get_auth_headers(aimhub_url):
    token_file_path = os.path.expanduser('~/.aimhub_user_token')
    if not os.path.exists(token_file_path):
        click.secho(f'Please login to AimHub server via `aim login {aimhub_url}` command.')
        exit(1)
    with open(token_file_path, 'r') as f:
        access_token = f.read()
    return {'Authorization': f'Bearer {access_token}'}
