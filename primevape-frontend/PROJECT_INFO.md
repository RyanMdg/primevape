# PrimeVape - Vape Shop E-Commerce Frontend

A modern, aesthetic e-commerce website for a vape shop built with React and Vite. Features a sleek black and white design theme.

## Features

- **Responsive Design**: Fully responsive layout that works on desktop, tablet, and mobile devices
- **Modern UI**: Clean black and white aesthetic with smooth animations and transitions
- **Product Catalog**: Browse products by category (Pods, E-Liquids, Accessories)
- **Product Details**: Detailed product pages with related products
- **Shopping Cart**: Full cart functionality with add/remove items and quantity adjustment
- **Category Filtering**: Easy navigation and filtering by product categories
- **Mobile Menu**: Touch-friendly mobile navigation

## Pages

1. **Home Page** - Hero section, category cards, and featured products
2. **Products Page** - Complete product catalog with category filters
3. **Product Detail Page** - Individual product information with related products
4. **Cart Page** - Shopping cart with checkout summary

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router DOM** - Client-side routing
- **React Icons** - Icon library (Feather Icons)
- **CSS3** - Custom styling with CSS variables

## Running the Project

The development server is currently running at: http://localhost:5173

## Project Structure

```
primevape-frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx       # Navigation header with cart badge
│   │   ├── Footer.jsx       # Footer with links and social media
│   │   └── ProductCard.jsx  # Reusable product card component
│   ├── pages/
│   │   ├── Home.jsx         # Home page
│   │   ├── Products.jsx     # Products listing page
│   │   ├── ProductDetail.jsx # Individual product page
│   │   └── Cart.jsx         # Shopping cart page
│   ├── data/
│   │   └── products.js      # Product data and categories
│   ├── App.jsx              # Main app component with routing
│   ├── index.css            # Global styles
│   └── main.jsx             # App entry point
```

## Design Theme

- **Primary Colors**: Black (#000000) and White (#FFFFFF)
- **Typography**: Modern sans-serif with uppercase headings
- **Interactions**: Smooth hover effects and transitions
