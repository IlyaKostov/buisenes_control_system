TAG_METADATA = [
    {
        'name': 'User | v1',
        'description': 'Operation with user v1.',
    },
    {
        'name': 'Company | v1',
        'description': 'Operation with company v1.',
    },
    {
        'name': 'healthz',
        'description': 'Standard health check.',
    },
]

TITLE = 'FastAPI Business Management System'
DESCRIPTION = (
    'Implemented on FastAPI.'
)
VERSION = '0.0.1'

ERRORS_MAP = {
    'mongo': 'Mongo connection failed',
    'postgres': 'PostgreSQL connection failed',
    'redis': 'Redis connection failed',
    'rabbit': 'RabbitMQ connection failed',
}