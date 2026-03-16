import requests

r = requests.post(
    'http://localhost:5000/api/admin/login',
    json={'username': 'admin', 'password': 'admin123'},
    headers={'X-API-KEY': 'ansh_aircool_secure_api_key_2026_change_in_production'}
)
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
