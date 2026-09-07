# Template Usage Guide

## Overview
This template creates luxury residential/hotel websites with a Mediterranean design aesthetic. The design is locked — only business data and images change.

## Quick Start
1. Replace business data in `src/config/business.js`
2. Replace images in `public/images/` folders
3. Open `index.html` in a browser

## Configuration Reference

### Business Data (src/config/business.js)
Document every field:
- `name` - Business name (displayed in header, footer, preloader)
- `tagline` - Short tagline
- `subtitle` - Section subtitle
- `address`, `city`, `region`, `postalCode`, `country`, `countryFull`, `area` - Location
- `whatsapp` - WhatsApp number (international format: +1234567890)
- `phone` - Phone number
- `email` - Contact email
- `website` - Website URL
- `googleMapsUrl` - Google Maps URL
- `bookingUrl` - Booking page URL
- `instagram`, `facebook` - Social media URLs
- `ogImage` - Open Graph image URL
- `heroImage` - Hero section background image
- `heroVideo` - Optional hero video
- `gallery` - Array of gallery images [{src, alt}]
- `apartments` - Array of apartment types [{id, type, rooms, areaMin, areaMax, image, features, description}]
- `amenities` - Array of amenities [{icon, name, description}]
- `faq` - Array of FAQ items [{question, answer}]

### Image Folders
```
public/images/
├── hero/          # Hero section background
├── gallery/       # Gallery grid images
├── rooms/         # Apartment type images
└── amenities/     # Amenity icons (optional, SVGs used by default)
```

### Recommended Image Sizes
- Hero: 1920x1080 or larger (landscape)
- Gallery: 1200x800 minimum
- Rooms: 960x640 minimum
- Amenity icons: 48x48 SVG

## Creating a New Hotel Website

### Step 1: Update Business Data
Open `src/config/business.js` and replace all fields with new hotel data.

### Step 2: Replace Images
1. Add hero image to `public/images/hero/`
2. Add room images to `public/images/rooms/`
3. Add gallery images to `public/images/gallery/`
4. Update image paths in `business.js`

### Step 3: Update WhatsApp
Set `whatsapp` to the hotel's WhatsApp number in international format.

### Step 4: Update Google Maps
Set `googleMapsUrl` to the hotel's Google Maps share URL.

### Step 5: Update Contact Info
Set `phone`, `email`, `website`, and social media URLs.

### Step 6: Update Content
Update `apartments`, `amenities`, and `faq` arrays with hotel-specific data.

## Customization

### Changing Colors
Edit CSS variables in `src/styles/main.css`:
```css
:root {
  --_colors---base-0--primary: #f5f0eb;  /* Background */
  --_colors---base-1000--primary: #1a1915;  /* Text */
}
```

### Changing Fonts
Update the Google Fonts link in `index.html` and CSS font-family.

### Adding Sections
Add new sections to `index.html` following the existing pattern.

## Deployment
- Static hosting (Netlify, Vercel, GitHub Pages)
- Upload all files
- No build step required

## Troubleshooting
- Images not loading: Check file paths in business.js
- WhatsApp not working: Ensure international format (+countrycode)
- Animations not working: Check browser console for JS errors
