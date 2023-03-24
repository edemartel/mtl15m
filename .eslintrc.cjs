// eslint-disable-next-line
module.exports = {
    'env': {
        'browser': true,
        'es2021': true
    },
    'extends': [
        'eslint:recommended',
        'plugin:vue/vue3-recommended',
        'plugin:@typescript-eslint/recommended'
    ],
    'overrides': [
    ],
    'parser': 'vue-eslint-parser',
    'parserOptions': {
        'parser': '@typescript-eslint/parser',
        'ecmaVersion': 'latest',
        'sourceType': 'module'
    },
    'plugins': [
        'vue',
        '@typescript-eslint'
    ],
    'rules': {
        'indent': [
            'error',
            4
        ],
        'quotes': [
            'error',
            'single'
        ],
        'semi': [
            'error',
            'always'
        ],
        'vue/html-self-closing': ['error', {
            'html': {
                'void': 'never',
                'normal': 'never',
                'component': 'never'
            }
        }]
    }
};
