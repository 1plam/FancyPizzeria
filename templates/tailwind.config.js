/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './components/**/*.{html,js}',
    './pages/**/*.{html,js}',
    './index.html',
    './menu.html',
    './menu.html',
    './order.html',
    './login.html',
    './signup.html',
    './payment.html',
    './kitchen.html',
    './modal.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('tailwindcss-aspect-ratio'),
    require('@tailwindcss/forms/tailwind.config'),
  ],
}

