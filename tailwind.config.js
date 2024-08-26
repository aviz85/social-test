module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
    './static/**/*.css',
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}