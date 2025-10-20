# cmis/data/symbols.py

SYMBOLS = {
    '∂': {
        'domain': 'calculus',
        'complexity': 0.7,
        'description': 'partial derivative operator'
    },
    '∫': {
        'domain': 'calculus',
        'complexity': 0.8,
        'description': 'integral symbol'
    },
    '∇': {
        'domain': 'calculus',
        'complexity': 0.9,
        'description': 'gradient operator'
    },
    'Σ': {
        'domain': 'statistics',
        'complexity': 0.6,
        'description': 'summation symbol'
    },
    '·': {
        'domain': 'linear_algebra',
        'complexity': 0.5,
        'description': 'dot product operator'
    },
    'F': {
        'domain': 'physics',
        'complexity': 0.4,
        'description': 'force variable'
    },
    'θ': {
        'domain': 'trigonometry',
        'complexity': 0.3,
        'description': 'angle variable'
    },
    'π': {
        'domain': 'geometry',
        'complexity': 0.2,
        'description': 'constant pi'
    }
}
