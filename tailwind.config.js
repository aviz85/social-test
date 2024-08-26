module.exports = {
  theme: {
    extend: {},
  },
  variants: {},
  plugins: [
    require('@tailwindcss/typography'),
  ],
  purge: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
}