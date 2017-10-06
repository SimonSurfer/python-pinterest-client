
PINS = {
    'fields': [
        'attribution',
        'board',
        'color',
        'counts',
        'created_at',
        'creator',
        'id',
        'image',
        'link',
        'media',
        'metadata',
        'note',
        'original_link',
        'url'
    ],
    'params': {
        'create': [
            ('board', True),  # Name of the parameter and is_required
            ('note', True),  # Name of the parameter and is_required
            ('link', False),  # Name of the parameter and is_required
            ('image', False),  # Name of the parameter and is_required
            ('image_url', False),  # Name of the parameter and is_required
            ('image_base64', False),  # Name of the parameter and is_required
        ],
        'update': [
            ('pin', True),  # Name of the parameter and is_required
            ('board', False),  # Name of the parameter and is_required
            ('note', False),  # Name of the parameter and is_required
            ('link', False),  # Name of the parameter and is_required
        ]
    }
}

BOARDS = {
    'fields': [
        'counts',
        'created_at',
        'creator',
        'description',
        'id',
        'image',
        'name',
        'privacy',
        'reason',
        'url'
    ],
    'params': {
        'create': [
            ('name', True),
            ('description', False),
        ],
        'update': [
            ('board', True),
            ('name', False),
            ('description', False),
        ]
    },
    'lists': {
        'pins': 'pins',
    }
}

ME = {
    'fields': [
        'account_type',
        'bio',
        'counts',
        'created_at',
        'first_name',
        'id',
        'image'
        'last_name',
        'url',
        'username',
    ],
    'lists': {
        'boards': 'boards',
        'pins': 'pins',
        'followers': 'users',
    }
}