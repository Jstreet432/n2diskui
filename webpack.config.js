const path = require('path');

module.exports = {
    entry: './n2diskui/static/js/filter_submit.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, './n2diskui/static/js')
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            }
        ]
    },
    mode: 'production'
};
