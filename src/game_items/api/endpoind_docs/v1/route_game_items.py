GET_GAME_ITEMS_RESPONSES = {
    401: {
        'description': "Not authenticated",
        'content': {
            'application/json': {
                'example': {'detail': "Not authenticated"}
            }
        }
    },
}

GET_GAME_ITEM_BY_ID_RESPONSES = {
    401: {
        'description': "Not authenticated",
        'content': {
            'application/json': {
                'example': {'detail': "Not authenticated"}
            }
        }
    },
    404: {
        'description': "Game items doesn't exist",
        'content': {
            'application/json': {
                'example': {'detail': "User with id %s doesn't exist"}
            }
        }
    },
}

POST_GAME_ITEMS_RESPONSES = {
    401: {
        'description': "Not authenticated",
        'content': {
            'application/json': {
                'example': {'detail': "Not authenticated"}
            }
        }
    },
    404: {
        'description': "Category not found. Create a new one",
        'content': {
            'application/json': {
                'example': {'detail': "Category with id: %s doesn't exist."}
            }
        }
    },
    409: {
        'description': "Name already exists try use other one.",
        'content': {
            'application/json': {
                'example': {'detail': "Name already exists."}
            }
        }
    },

}

PATCH_GAME_ITEMS_RESPONSES = {
    401: {
        'description': "Not authenticated",
        'content': {
            'application/json': {
                'example': {'detail': "Not authenticated"}
            }
        }
    },
    404: {
        'description': """
        1. Not existing Game item
        2. Not existing Game item category
        """,
        'content': {
            'application/json': {
                'examples': {
                    '1': {
                        'summary': 'Not existing Game item',
                        'value': {'detail': "The game item with id  %s doesn't exist."}
                    },
                    '2': {
                        'summary': 'Not existing Game item category',
                        'value': {'detail': "Category with id: %s doesn't exist."}
                    },
                },
            }
        }
    },
    409: {
        'description': 'Existing name',
        'content': {
            'application/json': {
                'example': {'detail': 'Name already exists'}
            }
        }
    }
}

DELETE_GAME_ITEMS_RESPONSES = {
    401: {
        'description': "Not authenticated",
        'content': {
            'application/json': {
                'example': {'detail': "Not authenticated"}
            }
        }
    },
    404: {
        'description': "Game items doesn't exist",
        'content': {
            'application/json': {
                'example': {'detail': "The game item with id  %s doesn't exist."}
            }
        }
    },
}
