# ERA Residence — Reference Structure

**Site:** www.era-residence.com
**Published:** Mon Jul 20 2026
**Platform:** Webflow
**Framework:** Barba.js (page transitions), GSAP (animations), Lenis (smooth scroll)
**Fonts:** Adobe Typekit (pig8glj)

---

## 1. Document Structure

```
<body class="body">
  <div data-barba="wrapper" class="transition-wrapper">
    <div class="main-css">
      <style> /* CSS custom properties + components */ </style>
    </div>

    <!-- Landscape cover (mobile landscape lock) -->
    <div class="landscape-cover">

    <!-- Master preloader -->
    <div data-master-preloader="" class="master-preloader theme_on-dark">

    <!-- Preloader -->
    <div data-preloader="" class="preloader theme_on-dark">

    <!-- Cookies banner -->
    <div data-cookies="" class="cookies">

    <!-- Main content -->
    <main data-barba-namespace="home" data-barba="container" class="transition-container">
      <div class="theme_on-color">
        <a href="#hero" class="header-logo w-inline-block">
        <div class="header-nav">
        <div class="s-bar-w">
        <div class="s-down">

        <!-- Sections here -->

      </div>
    </main>
  </div>
</body>
```

---

## 2. Sections in Order

| # | Section | ID/Class | Description |
|---|---------|----------|-------------|
| 1 | **Preloader** | `[data-preloader]` `.preloader` | Animated loading screen with logo, text, progress bar |
| 2 | **Hero** | `#hero` `.section.clip.theme_on-color` | Full-viewport hero with day/night tabs, title, pins |
| 3 | **Benefits Intro (Arch)** | `.section.arch.clip.theme_on-brand` | "Costa del Sol" logo + circular text SVG |
| 4 | **Benefits/Quote** | `data-bg="light" data-snap="" .section.z-2.theme_on-brand` | Slider with 3 benefit cards + quote section |
| 5 | **Location Horizontal Scroll** | `data-bg="light" data-slow-scroll="" .section.clip` | Horizontal scrolling location section with video |
| 6 | **Location Intro** | `.loc-intro-w` | "New Golden Mile" title + terrace image |
| 7 | **Location Path** | `.loc-path-w` | SVG path/map with labels |
| 8 | **Location Background** | `data-parallax="img" .loc-w_bg` | Master plan image with parallax |
| 9 | **Apartment Types** | `data-bg="light" data-snap="" .section.theme_on-brand` | CMS-driven apartment type slider |
| 10 | **Apartment Info** | `data-bg="light" .section.clip.theme_on-brand` | "A place to live" + description + logo |
| 11 | **Amenities** | `.section.clip.theme_on-color` | Tabbed amenities (Gated Community, Pool & Wellness, etc.) |
| 12 | **Interior/Gallery** | `.section.arch.clip` | "The space to Live in" + gallery slider |
| 13 | **Architecture** | `.section.clip` | "Architecture" horizontal scroll with images |
| 14 | **Other/FAQ** | `data-bg="light" .section.clip` | Accordion cards (Developer, Sales, License, Timeline) |
| 15 | **CTA** | `data-bg="color" .section.theme_on-color` | "Perfect sea views" CTA with form trigger |
| 16 | **Footer** | `data-bg="dark" .section.theme_on-dark` | Contact info, social links, legal |
| 17 | **Modals** | `.modal` | Book a Call form, Mobile menu |

---

## 3. Typography Classes

### Heading Hierarchy
| Class | Usage |
|-------|-------|
| `.h1` | Main headings (hero title "Era Residence", section titles) |
| `.h2` | Secondary headings (mobile benefit titles, nav) |
| `.h3` | Tertiary headings (apartment titles, footer phone) |
| `.h4` | Quarter headings (circular SVG text, quotes) |
| `.h5` | Quinary headings (hero subtitle, quote body text) |
| `.h6` | Small headings (nav items, links, buttons) |

### Body/Label Classes
| Class | Usage |
|-------|-------|
| `.c1` | Caption/label text ("Costa", "del Sol", "Spain", "Cookies") |
| `.a1` | Accent text large (hero "Estepona", preloader "Estepona") |
| `.a2` | Accent text medium (book-a-call title, preloader title) |
| `.l1` | Body/label text large (descriptions, nav items, form labels) |
| `.l2` | Body/label text small (menu items, "Scroll", "To top") |
| `.p1` | Paragraph text (body copy, descriptions) |

### Typography Modifiers
| Modifier | Usage |
|----------|-------|
| `.reg` | Regular weight variant (labels, captions) |
| `.a-center` | Text center alignment |
| `.a-left` | Text left alignment |
| `.a-right` | Text right alignment |
| `.mob_a-center` | Center alignment on mobile only |
| `.mob_a-right` | Right alignment on mobile only |
| `.no-wrap` | Prevent text wrapping |

### Split Text Classes (GSAP SplitText)
| Class | Purpose |
|-------|---------|
| `.split-line` | Split by line |
| `.split-word` | Split by word |
| `.split-char` | Split by character |
| `.split-line-mask` | Line mask wrapper |
| `.split-word-mask` | Word mask wrapper |
| `.split-char-mask` | Character mask wrapper |

---

## 4. Color Variables (CSS Custom Properties)

### Base Colors
```css
--_colors---base-0--primary       /* Light background (white/cream) */
--_colors---base-1000--primary     /* Dark text (near-black) */
--_colors---base-1000--100         /* Darkest variant */
--_colors---base-1000--line        /* Border/line color */
--_colors---other--bg              /* Selection background */
--_colors---other--transparent     /* Transparent */
--_colors---base-1000--bg          /* Hover state background */
```

### Theme System
The site uses a theme switching system with CSS classes:

| Theme Class | Usage |
|-------------|-------|
| `.theme_on-color` | Standard light theme (hero, preloader, amenities, CTA) |
| `.theme_on-brand` | Brand/accent theme (benefits, apartments, interior) |
| `.theme_on-dark` | Dark theme (footer, modals, preloader) |
| `.theme_on-light` | Light theme variant |

Theme affects: `.l1`, `.l2`, `.h6`, `.logo`, `.header-logo_bg`, `.s-down_arrow`, `.s-bar_track`, `.s-bar_fill`

---

## 5. Layout System

### Grid
The site uses a Webflow grid system:
```html
<div class="grid">
  <div class="grid _4-columns">    <!-- 4-column variant -->
  <div class="grid _5-columns">    <!-- 5-column variant -->
  <div class="grid _6-columns">    <!-- 6-column variant -->
  <div class="grid _8-columns">    <!-- 8-column variant -->
  <div class="grid _13-columns">   <!-- 13-column variant -->
  <div class="grid fill">          <!-- Full-width variant -->
```

### Container
```html
<div class="container">
```

### Spacing Utilities (Units)
| Class | Usage |
|-------|-------|
| `.u-4` | 4px spacing |
| `.u-8` | 8px spacing |
| `.u-12` | 12px spacing |
| `.u-16` | 16px spacing |
| `.u-24` | 24px spacing |
| `.u-32` | 32px spacing |
| `.u-48` | 48px spacing |
| `.u-64` | 64px spacing |
| `.u-96` | 96px spacing |
| `.u-160` | 160px spacing |
| `.u-272` | 272px spacing (mobile only, large vertical gap) |
| `.u-48` | 48px spacing |

### CSS Custom Units
```css
--_units---u-0       /* 0 */
--_units---u-4       /* 4px */
--_units---u-8       /* 8px */
--_units---u-16      /* 16px */
--_units---u-24      /* 24px */
--_units---u-32      /* 32px */
--_units---u-160     /* 160px */
--_special-units---scale-ratio     /* Scale ratio for rem calculations */
--_special-units---offset-l        /* Left offset */
--_special-units---offset-r        /* Right offset */
```

---

## 6. Navigation Structure

### Header
```html
<a href="#hero" class="header-logo w-inline-block">
  <div class="logo_symbol header">
    <div class="logo w-embed"><!-- SVG logo --></div>
  </div>
  <div class="header-logo_bg b-desk w-embed"><!-- Decorative bg SVG --></div>
  <div class="header-logo_bg b-mob w-embed"><!-- Mobile variant --></div>
</a>

<div class="header-nav">
  <!-- Mobile nav -->
  <div class="header-nav_list f-mob">
    <div class="btn-menu">
      <div class="btn-menu_label is-active"><!-- "Menu" --></div>
      <div class="btn-menu_label"><!-- "Close" --></div>
      <div class="ico-24"><!-- Hamburger icon --></div>
    </div>
  </div>

  <!-- Desktop nav -->
  <div class="header-nav_list f-desk">
    <a href="/apartments" class="link"><!-- "Select an Apartment" --></a>
    <a data-modal-cta-btn="book-a-call" class="nav-item"><!-- "Book a call" --></a>
    <a href="/contact" class="nav-item"><!-- "Contact" --></a>
  </div>
</div>
```

### Navigation Items Pattern
```html
<a hover-nav-item-l2="" class="nav-item w-inline-block">
  <div class="nav-item_label">
    <div hover="text" class="nav-item_label_text">
      <div class="l2">Menu</div>           <!-- Visible state -->
    </div>
    <div hover="text" class="nav-item_label_text is-2">
      <div class="l2">Close</div>          <!-- Hover state -->
    </div>
  </div>
</a>
```

### Scroll Bar (Progress Indicator)
```html
<div data-s-bar="" class="s-bar">
  <div data-s-bar-thumb="" class="s-bar_thumb">
    <div data-s-bar-label="" class="l1 a-center">00</div>
  </div>
  <div data-s-bar-fill="" class="s-bar_fill"></div>
  <div data-s-bar-track="" class="s-bar_track"></div>
</div>
```

### Scroll Down Arrow
```html
<div class="s-down">
  <div class="s-down_arrow w-embed"><!-- Arrow SVG --></div>
  <div class="l2">Scroll</div>
</div>
```

---

## 7. Animation Classes & Data Attributes

### Data Attributes
| Attribute | Purpose |
|-----------|---------|
| `data-parallax="img"` | Parallax on images |
| `data-parallax="img-out"` | Outward parallax on images |
| `data-parallax="img-in"` | Inward parallax on images |
| `data-parallax="w"` | Parallax on wrapper |
| `data-parallax="ctn-down"` | Downward parallax on container |
| `data-parallax="ctn-up"` | Upward parallax on container |
| `data-scroll-reveal="a"` | Scroll reveal - accent text |
| `data-scroll-reveal="h"` | Scroll reveal - heading |
| `data-scroll-reveal="p"` | Scroll reveal - paragraph |
| `data-scroll-reveal="slide"` | Scroll reveal - slide in |
| `data-scroll-reveal="ctn"` | Scroll reveal - container |
| `data-scroll-reveal="line"` | Scroll reveal - line |
| `data-prevent-flicker` | Prevent flicker during load |
| `data-snap` | Section snapping |
| `data-slow-scroll` | Slow scroll section |
| `data-scroll-horizontal` | Horizontal scroll container |
| `data-tabs` | Tab system |
| `data-tabs-hero` | Hero-specific tabs |
| `data-tabs-hilight="ver"` | Vertical highlight tabs |
| `data-tab-trigger="day"` / `"night"` | Tab trigger |
| `data-tab-content="day"` / `"night"` | Tab content |
| `data-tab="img"` / `"p"` / `"slide"` | Tab child elements |
| `data-bg="color"` / `"light"` / `"dark"` | Theme background |
| `data-theme` | Theme toggle element |
| `data-video-playpause` | Video play/pause on scroll |
| `data-pin="..."` | Hero image pin |
| `data-pin-pulse` | Pin pulse animation |
| `data-cookies` | Cookie consent |
| `data-marquee-css` | CSS marquee animation |
| `data-marquee-css="track"` | Marquee track |
| `data-ico-plus` | Plus/minus icon toggle |
| `data-accordion-card` | Accordion card |
| `data-accordion-card="content"` | Accordion content |
| `data-accordion-card="p"` | Accordion paragraph |
| `data-accordion-card="ctn"` | Accordion container |
| `data-select` | Custom select dropdown |
| `data-select="btn"` | Select button |
| `data-select="drop-down"` | Select dropdown |
| `data-hover-group` | Hover group container |
| `data-hover-item` | Hover group item |
| `data-slider` | Slider container |
| `data-slider="slide"` | Slider slide |
| `data-slider="pag"` | Slider pagination |
| `data-slider="prev"` / `"next"` | Slider navigation |
| `data-slider="current"` / `"next-num"` | Slider numbers |
| `data-slider="progress"` | Slider progress bar |
| `data-slider="h"` / `"p"` / `"img"` | Slider child elements |
| `data-reveal-first` | First slide reveal |
| `data-reset` | Reset/disable state |
| `data-comma` / `data-comma-list` | Comma-separated list |
| `data-circle-text` | Circular SVG text |
| `data-text` | Text element for animations |
| `data-fit-text` | Auto-fit text |
| `data-master-preloader` | Master preloader |
| `data-preloader` | Page preloader |
| `data-part="h"` / `"a"` / `"p"` / `"line"` / `"ctn"` | Preloader animation parts |

### Hover System Attributes
| Attribute | Purpose |
|-----------|---------|
| `hover-btn` | Button hover effect |
| `hover-btn-circle` | Circle button hover |
| `hover-nav-item-l2` | Navigation item L2 hover |
| `hover-nav-item-l2-trigger` | Navigation trigger |
| `hover-img-card` | Image card hover |
| `hover-apart-card` | Apartment card hover |
| `hover-social` | Social icon hover |
| `hover-social-trigger` | Social trigger |
| `hover-media-item` | Media item hover |
| `hover-tab` | Tab hover |
| `hover-link` | Link hover |
| `hover-pin` | Map pin hover |
| `hover-pin-trigger` | Pin trigger |
| `hover-select-item` | Select item hover |
| `hover-nav-item` | Navigation item hover |

### Hover Child Elements
| `hover` value | Purpose |
|---------------|---------|
| `hover="text"` | Text element (color change) |
| `hover="bg"` | Background element (fill animation) |
| `hover="ico"` | Icon element (scale/rotation) |
| `hover="img"` | Image element (scale) |
| `hover="btn"` | Button element (opacity) |

### Active State Classes
| Class | Purpose |
|-------|---------|
| `.is-active` | Active state (tabs, pins, accordion, select) |
| `.is-open` | Open state (dropdowns) |
| `.is-disabled` | Disabled state |
| `.is-day` / `.is-night` | Day/night tab state |
| `.is-top` | Top scroll position state |
| `.is-2` | Second state (hover text layer) |

### Marquee
```html
<div data-marquee-css="">
  <div data-marquee-css="track">
    <!-- Duplicated content for seamless loop -->
  </div>
</div>
```
Animation: `@keyframes marquee { from { transform: translateX(-50%); } to { transform: translateX(0%); } }`
Duration: 32s linear infinite reverse

---

## 8. Image Sizing & Aspect Ratios

### Image Wrapper Pattern
```html
<div class="img-w">
  <img class="img" src="..." alt="..." loading="eager" />
</div>
<div class="img-w h-auto">
  <img class="img h-auto" src="..." alt="..." loading="eager" />
</div>
```

### Image Classes
| Class | Purpose |
|-------|---------|
| `.img` | Base image |
| `.img.contain` | `object-fit: contain` |
| `.img.h-auto` | `height: auto` |
| `.img-p` | Portrait/vertical image |
| `.img-w` | Image wrapper |
| `.img-over-grad` | Gradient overlay |
| `.img-over-grad.from-bot` | Gradient from bottom |
| `.img-over-grad.from-top` | Gradient from top |
| `.img-over-grad.bot._4x` | Bottom gradient 4x height |
| `.img-over-grad.bot._100vh` | Bottom gradient full viewport |
| `.img-over-grad._100vh` | Full viewport gradient |

### Responsive Images
All images use Webflow's `srcset` with breakpoints:
- 500w, 800w, 1080w, 1600w, 1920w
- `sizes="(max-width: 1920px) 100vw, 1920px"`

---

## 9. Mobile vs Desktop Behavior

### Visibility Classes
| Class | Purpose |
|-------|---------|
| `.b-mob` | **Mobile only** (hidden on desktop) |
| `.b-desk` | **Desktop only** (hidden on mobile) |

### Breakpoint
```css
@media (min-width: 992px) { /* Desktop */ }
@media (max-width: 991px) { /* Mobile/Tablet */ }
```

### Key Mobile Differences
- Preloader titles stack vertically
- Hero title smaller
- Navigation becomes hamburger menu
- Section spacing increases (`.u-272` on mobile)
- Horizontal scroll sections become vertical
- Logo background SVGs have mobile-specific variants (80x80 vs 120x120)
- Architecture section hides desktop version
- Gallery layout adjusts

### Landscape Lock
```css
@media screen and (orientation: landscape) and (max-width: 991px) and (pointer: coarse) and (hover: none) {
  .landscape-cover { display: block; }
  body { overflow: hidden; }
}
```

---

## 10. Preloader Structure

```html
<div data-preloader="" class="preloader theme_on-dark">
  <div class="preloader_ctn">
    <div class="preloader_t">
      <div class="u-48"></div>
      <div class="s_logo">
        <div data-part="ctn" class="logo_symbol ico-48">
          <div class="logo w-embed"><!-- SVG logo --></div>
        </div>
      </div>
    </div>
    <div class="preloader_c">
      <div class="grid">
        <div class="preloader_title-l">
          <div data-part="h" class="c1 a-center">Costa</div>
        </div>
        <div class="preloader_logo">
          <div data-part="h" class="h3 a-center">Era<br/>Residence</div>
          <div class="preloader_logo_a">
            <div data-part="a" class="a2 preloader_a a-center">Estepona</div>
          </div>
        </div>
        <div class="preloader_title-r">
          <div data-part="h" class="c1 a-center">del Sol</div>
        </div>
      </div>
    </div>
    <div class="preloader_b">
      <div class="grid">
        <div class="s_title">
          <div data-part="line" class="preloader_progress">
            <div class="preloader_progress_fill">
              <div class="preloader_progress_track"></div>
            </div>
          </div>
          <div class="u-32"></div>
          <p data-part="p" class="l1 a-center">Era Residence<br/>A place to return to.</p>
        </div>
      </div>
    </div>
  </div>
  <div class="preloader_bg_arch">
    <div class="preloader_bg_arch_is-1"></div>
    <div class="preloader_bg_arch_is-2"></div>
  </div>
  <div class="preloader_bg">
    <div class="preloader_bg_a">
      <img src="..." alt="" class="img" />
    </div>
    <div class="preloader_bg_decor">
      <div data-wf--decor--variant="large" class="decor"><!-- Corner decorations --></div>
    </div>
  </div>
</div>
```

### Preloader Animation
- `data-part="h"`: Heading text animation
- `data-part="a"`: Accent text animation
- `data-part="p"`: Paragraph text animation
- `data-part="line"`: Progress bar animation
- `data-part="ctn"`: Container animation

### Arch Mask
The preloader uses a complex CSS mask with an SVG arch shape:
```css
[data-preloader] {
  mask-image: ... url('preloader_arch-l.svg');
  mask-size: calc(50% - (var(--arch-w) / 2) + 2px) 100%, ...;
}
```

---

## 11. Button/Link Patterns

### Standard Link
```html
<a hover-link="" href="#" class="link w-inline-block">
  <div class="link_label">
    <div class="link_label_text">
      <div hover="text" class="h6">Text</div>
    </div>
    <div class="link_label_text is-2">
      <div hover="text" class="h6">Text</div>
    </div>
  </div>
</a>
```

### Button with Background Fill
```html
<a hover-btn="" href="#" class="btn w-inline-block">
  <div hover="bg" class="btn_bg"></div>
  <div hover="text" class="btn_text">Button Text</div>
</a>
```

### Circle Button (CTA)
```html
<div data-scroll-reveal="ctn" class="cta-s_title_btn">
  <div hover-btn-circle="" class="btn-circle">
    <div class="btn-circle_c">
      <svg><!-- Circle SVG with arc --></div>
      <a href="/apartments" class="btn-circle_link w-inline-block"></a>
    </div>
  </div>
</div>
```

### Social Link
```html
<a hover-social="" href="..." target="_blank" class="social-btn w-inline-block">
  <div hover="ico" class="ico-16">
    <div class="ico w-embed"><!-- Icon SVG --></div>
  </div>
  <div data-comma="" class="social-btn_line">
    <div class="line-h"></div>
  </div>
</a>
```

### Nav Item
```html
<a hover-nav-item-l2="" class="nav-item w-inline-block">
  <div class="nav-item_label">
    <div hover="text" class="nav-item_label_text">
      <div class="l2">Label</div>
    </div>
    <div hover="text" class="nav-item_label_text is-2">
      <div class="l2">Label</div>
    </div>
  </div>
</a>
```

---

## 12. Form Structure

### Book a Call Modal
```html
<div id="book-a-call" class="modal_cta_form w-form">
  <form id="wf-form-Book-a-call" name="wf-form-Book-a-call" data-name="Book a call" method="post">
    <div class="modal_cta_l">
      <div class="modal_cta_l_t">
        <div class="modal_cta_a">
          <h1 class="a2 b-desk">Book a call</h1>
          <div class="a1 b-mob">Book a call</div>
        </div>
      </div>
      <div class="modal_cta_l_b">
        <p class="l1 mob_a-center">Leave your details...</p>
      </div>
    </div>

    <div class="modal_cta_c_c">
      <div class="modal_cta_c_line"><div class="line-v"></div></div>
      <div class="modal_cta_c_logo"><!-- Logo --></div>
      <div class="modal_cta_c_line"><div class="line-v"></div></div>
    </div>

    <div class="modal_cta_r">
      <div class="modal_cta_form_c">
        <div class="form_block_list">
          <input class="d-none w-input" name="title" type="text" /> <!-- Hidden -->
          <div class="input">
            <div class="input_label">
              <label for="name" class="l1 reg">Name:</label>
            </div>
            <input class="input_field l1 w-input" name="name" type="text" required />
          </div>
          <div class="input">
            <div class="input_label">
              <label for="email" class="l1 reg">Email:</label>
            </div>
            <input class="input_field l1 w-input" name="email" type="email" required />
          </div>
          <div class="input">
            <div class="input_label">
              <label for="phone" class="l1 reg">Phone:</label>
            </div>
            <input class="input_field l1 w-input" name="phone" type="tel" required />
          </div>
          <div class="input">
            <div class="input_label">
              <label for="message" class="l1 reg">Message:</label>
            </div>
            <textarea class="input_field area l1 w-input" name="message" maxlength="5000"></textarea>
          </div>
          <!-- Hidden UTM fields -->
          <input class="d-none w-input" name="utm_source" type="text" />
          <input class="d-none w-input" name="utm_medium" type="text" />
          <input class="d-none w-input" name="utm_campaign" type="text" />
          <input class="d-none w-input" name="utm_content" type="text" />
          <input class="d-none w-input" name="page_url" type="text" />
          <input class="d-none w-input" name="user_agent" type="text" />
          <input class="d-none w-input" name="timestamp" type="text" />
          <input type="submit" value="Send" class="btn w-button" />
        </div>
      </div>
    </div>
  </form>
  <div class="form_success_desc">
    <p class="p1 a-center">Our sales manager will review your message...</p>
  </div>
  <div class="form_error theme_on-dark w-form-fail">
    <div class="l1 a-center">Oops! Something went wrong...</div>
  </div>
</div>
```

### Input Classes
| Class | Purpose |
|-------|---------|
| `.input` | Input wrapper |
| `.input_label` | Label wrapper |
| `.input_field` | Input/textarea base |
| `.input_field.area` | Textarea variant |
| `.input_field.l1` | Large input variant |
| `.d-none` | Hidden input |

---

## 13. Slider/Carousel Pattern

### Slider Container
```html
<div data-slider="" class="[section]_cms">
  <div class="[section]_cms_pag">
    <div data-scroll-reveal="ctn" data-slider="pag" class="pag">
      <div data-slider="prev" class="pag_prev">
        <div class="ico-16"><!-- Left arrow SVG --></div>
        <div class="pag_prev_label">
          <div data-slider="current" class="l1">00</div>
        </div>
      </div>
      <div class="pag_progress">
        <div data-slider="progress" class="pag_progress_fill"></div>
      </div>
      <div data-slider="next" class="pag_next">
        <div class="pag_prev_label">
          <div data-slider="next-num" class="l1">00</div>
        </div>
        <div class="ico-16"><!-- Right arrow SVG --></div>
      </div>
    </div>
  </div>

  <div class="[section]-cms w-dyn-list">
    <div role="list" class="[section]-cms_list w-dyn-items">
      <div data-reveal-first="" data-slider="slide" role="listitem" class="[item] w-dyn-item">
        <!-- Slide content with data-slider="h", data-slider="p", data-slider="img" -->
      </div>
    </div>
  </div>
</div>
```

### Slider Types Found
1. **Benefits Slider** (`benefits-s_cms`) — 3 benefit slides
2. **Apartment Type Slider** (`apart-type-s_cms`) — CMS apartment types
3. **Gallery Slider** (`interior-s_gallery-cms`) — Interior gallery images
4. **Amenities Slider** (tab-based, not carousel)

---

## 14. Hero Section Structure

```html
<section id="hero" class="section clip theme_on-color">
  <div class="container">
    <div class="hero-scroll-area">
      <div data-tabs-hero="" class="hero-w">
        <div class="hero-s">
          <h1 data-prevent-flicker="" data-scroll-reveal="h" class="h1 a-center">
            Era <br/>Residence
          </h1>
          <h2 data-prevent-flicker="" data-scroll-reveal="a" class="a2">Estepona</h2>
          <h3 class="hero-s_title h5">
            <span data-scroll-reveal="h">A place</span>
            <div data-scroll-reveal="ctn" class="hero-s_tabs">
              <a data-tab-trigger="day" class="nav-item">by day</a>
              <div class="hero-s_tabs_divider"></div>
              <a data-tab-trigger="night" class="nav-item">by night</a>
            </div>
            <span data-scroll-reveal="h">to return to</span>
          </h3>
        </div>

        <div class="hero-w_bg">
          <div class="hero-w_bg_master">
            <!-- Desktop pins -->
            <div class="pins-cms b-desk w-dyn-list">
              <div data-pin="crafted-to-endure" class="pin">...</div>
              <div data-pin="light-flow" class="pin">...</div>
              <div data-pin="your-private-sanctuary" class="pin">...</div>
            </div>
            <!-- Day image -->
            <div data-tab-content="day" class="hero-w_bg_master_img_day">
              <img src="...gated-community_day.webp" class="img h-auto hero-img" />
            </div>
            <!-- Night image -->
            <div data-tab-content="night" class="hero-w_bg_master_img_night">
              <img src="...gated-community_night.webp" class="img h-auto hero-img" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="hero_themes">
    <div data-bg="color" class="hero_themes_color"></div>
    <div data-bg="light" class="hero_themes_light"></div>
  </div>
</section>
```

---

## 15. Amenities Section (Tab-Based)

```html
<section class="section clip theme_on-color">
  <div class="container">
    <div class="amen-w">
      <div data-tabs-hilight="ver" data-tabs="" class="amen-s_cms">
        <!-- Tab content items -->
        <div data-tab-content="gated-community" class="amen-cms_list_item">
          <div class="amen-slide">
            <div class="amen-slide_b">
              <h3 data-tab="p" class="l1">Gated community</h3>
              <div class="red-line"></div>
              <h4 data-tab="p" class="h5">Description text...</h4>
            </div>
            <div class="amen-slide_img">
              <img data-parallax="img-in" class="img" />
            </div>
          </div>
        </div>
        <!-- More tabs: pool-wellness, architecture-design, built-to-last -->
      </div>
    </div>
  </div>
</section>
```

### Tab States
```css
.amen-tab {
  opacity: 0.4;  /* Default */
  &:hover { opacity: 1; }  /* Desktop hover */
  &.is-active { opacity: 1; }  /* Active */
}
```

---

## 16. Accordion/FAQ Pattern

```html
<div data-accordion-card="" class="other-card">
  <div class="other-card_name">
    <div class="other-card_name_label">
      <h4 data-scroll-reveal="h" class="h3 a-center">Developer</h4>
      <div data-scroll-reveal="ctn" data-ico-plus="" class="other-card_ico">
        <div class="ico-16"><!-- Plus icon SVG --></div>
      </div>
    </div>
  </div>
  <div data-accordion-card="content" class="other-card_info">
    <div class="grid _6-columns">
      <div class="other-card_info_desc">
        <p data-accordion-card="p" class="p1 a-center">Description...</p>
        <div data-accordion-card="ctn" class="info_divider">
          <div class="line-h"></div>
        </div>
      </div>
    </div>
  </div>
</div>
```

### Accordion Items
1. **Developer** — Swiss Technology S.L.
2. **Sales & Marketing** — Unreal Estate Group (with logo)
3. **License obtained** — Full permits documentation
4. **2026** — Construction timeline

---

## 17. Footer Structure

```html
<section data-bg="dark" class="section theme_on-dark">
  <div class="container">
    <div class="footer-w">
      <!-- Back to top -->
      <a href="#hero" class="footer-s_s-top w-inline-block">
        <div class="l2">To top</div>
        <div class="s-down_arrow"><!-- Arrow SVG --></div>
      </a>

      <div class="footer-s">
        <!-- Top: Contact -->
        <div class="footer-s_c">
          <div class="grid">
            <div class="footer-s_contact">
              <div class="s_logo">
                <div class="logo_symbol ico-64"><!-- Logo SVG --></div>
              </div>
              <div class="contact-cms w-dyn-list">
                <a href="tel:+34655408648" class="nav-item">
                  <div class="h2 a-center">+34 (655) 408-648</div>
                </a>
              </div>
            </div>

            <div class="footer-s_address">
              <div class="loc-cms w-dyn-list">
                <h3 class="l1 reg a-center">Sales Office</h3>
                <a href="https://maps.app.goo.gl/..." class="nav-item">
                  <div class="l1">Avenida Litoral, 29680 Estepona, Málaga, Spain</div>
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Bottom: Legal + Social -->
        <div class="footer-s_b">
          <div class="grid">
            <div class="footer-s_info">
              <div class="l1">Era Residence.</div>
              <div class="l1 reg no-wrap">&copy;<span class="year">2026</span> All rights reserved</div>
              <div class="legal-cms w-dyn-list">
                <a href="...pdf" class="nav-item">Privacy policy</a>
                <a href="...pdf" class="nav-item">Legal notice</a>
              </div>
            </div>

            <div class="social-cms w-dyn-list">
              <a href="https://linkedin.com/..." class="social-btn"><!-- LinkedIn --></a>
              <a href="https://facebook.com/..." class="social-btn"><!-- Facebook --></a>
              <a href="https://instagram.com/..." class="social-btn"><!-- Instagram --></a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## 18. Modal Structure

### Book a Call Modal
```html
<div data-modal-cta="book-a-call" class="modal modal-cta theme_on-dark">
  <div data-modal-container="" class="modal_c">
    <div data-modal-close="" class="modal_close"><!-- Close button --></div>
    <!-- Form content -->
  </div>
  <div data-modal-close="" data-modal-over="" class="modal_over"></div>
</div>
```

### Mobile Menu Modal
```html
<div data-modal-menu="mob" class="modal menu theme_on-dark">
  <div class="modal_c">
    <div data-modal-container="" class="modal_menu">
      <div class="modal_menu_t">
        <div class="h1 a-center">Menu</div>
      </div>
      <div class="modal_menu_c">
        <a href="/" class="link">Home</a>
        <a href="/apartments" class="link">Select an Apartment</a>
        <a data-modal-cta-btn="book-a-call" class="link">Book a call</a>
        <a href="/contact" class="link">Contact</a>
      </div>
    </div>
  </div>
  <div data-modal-close="" data-modal-over="" class="modal_bg"></div>
</div>
```

---

## 19. Decorative Elements

### Corner Decorations
```html
<div data-wf--decor--variant="large" class="decor">
  <div class="frame_l-tb w-embed"><!-- Vertical line --></div>
  <div class="frame_lt w-embed"><!-- Diagonal line \ --></div>
  <div class="frame_t-lr w-embed"><!-- Horizontal line --></div>
  <div class="frame_rt w-embed"><!-- Diagonal line / --></div>
  <div class="frame_r-tb w-embed"><!-- Vertical line --></div>
  <div class="frame_rb w-embed"><!-- Diagonal line \ --></div>
  <div class="frame_b-lr w-embed"><!-- Horizontal line --></div>
  <div class="frame_lb w-embed"><!-- Diagonal line / --></div>
</div>
```

Variants: `large`, `med` (w-variant-db77920b-274b-9558-1ced-34e87f5b7d94)

### Divider Lines
```html
<div class="divider">
  <div data-scroll-reveal="line" class="line-v"></div>  <!-- Vertical -->
</div>
<div class="line-h"></div>  <!-- Horizontal -->
<div class="red-line"></div>  <!-- Red accent line -->
```

### Flower Videos (Bougainvillea)
```html
<div data-parallax="ctn-down" class="flower [section]">
  <video muted="" playsinline="" loop="" disablepictureinpicture=""
         poster="...avif" class="video">
    <source src="...webm" type="video/webm" />
    <source src="...mov" type="video/mp4" />
  </video>
</div>
```

Flower positions: `.flower.loc-info`, `.flower.loc-intro`, `.flower.loc-path`, `.flower.interior`, `.flower.arch-intro-l`, `.flower.arch-intro-r`, `.flower.apart-info`, `.flower.other`

---

## 20. Easing & Duration Variables

```css
:root {
  --dur-s: 0.4s;      /* Short duration */
  --dur-m: 0.8s;      /* Medium duration */
  --dur-l: 1.2s;      /* Long duration */

  --ease-in-out: cubic-bezier(0.76, 0, 0.24, 1);
  --ease-out: cubic-bezier(0.25, 1, 0.5, 1);
  --ease-in: cubic-bezier(0.5, 0, 0.75, 0);
  --ease: cubic-bezier(0.25, 0.1, 0.25, 1);
  --ease-write: cubic-bezier(0.333, 0, 0.667, 1);

  --_100svh: 100vh;
}
```

### Component Durations
```css
--btn-dur: var(--dur-m);           /* 0.8s */
--nav-item-l2-dur: var(--dur-m);  /* 0.8s */
--card-dur: var(--dur-l);          /* 1.2s */
--apart-card-dur: 1.6s;           /* 1.6s */
--social-dur: var(--dur-m);       /* 0.8s */
--media-item-dur: var(--dur-s);   /* 0.4s */
--select-dur: var(--dur-m);       /* 0.8s */
--select-item-dur: var(--dur-s);  /* 0.4s */
--pin-dur: var(--dur-m);          /* 0.8s */
--pag-dur: var(--dur-m);          /* 0.8s */
```

---

## 21. Responsive Breakpoints

| Breakpoint | Value | Usage |
|------------|-------|-------|
| Desktop | `min-width: 992px` | Hover effects, desktop layout |
| Mobile/Tablet | `max-width: 991px` | Mobile layout, touch devices |
| Landscape Lock | `orientation: landscape AND max-width: 991px AND pointer: coarse AND hover: none` | Forces portrait lock screen |

---

## 22. CSS Reset

```css
html, body, div, span, applet, object, iframe, h1-h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s,
samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, dl, dt, dd,
ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead,
tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer,
header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {
  margin: 0; padding: 0; border: 0; vertical-align: baseline;
}
article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
  display: block;
}
body { line-height: 1; }
ol, ul { list-style: none; }
blockquote, q { quotes: none; }
table { border-collapse: collapse; border-spacing: 0; }
```

---

## 23. Selection Style

```css
::selection {
  color: var(--_colors---other--bg);
  background: var(--_colors---base-1000--primary);
}
```

---

## 24. Scrollbar

```css
.scrollbar-none::-webkit-scrollbar { display: none; }
```

---

## 25. External Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| GSAP | 3.15 | Animation engine |
| ScrollTrigger | 3.15 | Scroll-based animations |
| SplitText | 3.15 | Text splitting for animations |
| CustomEase | 3.15 | Custom easing curves |
| Lenis | 1.3.21 | Smooth scrolling |
| Barba.js | (latest) | Page transitions |
| Lottie | 5.12.2 | Lottie animations |
| jQuery | 3.5.1 | DOM manipulation (Webflow) |
| Typekit | pig8glj | Adobe fonts |

---

## 26. Webflow-Specific Classes

| Class | Purpose |
|-------|---------|
| `.w-inline-block` | Inline-block display |
| `.w-input` | Form input styling |
| `.w-button` | Button styling |
| `.w-form-fail` | Form error state |
| `.w-dyn-list` | CMS collection list |
| `.w-dyn-items` | CMS collection items |
| `.w-dyn-item` | CMS collection item |
| `.w-dyn-empty` | Empty CMS state |
| `.w-embed` | Embed wrapper |
| `.w-variant-*` | Webflow variant classes |

---

## 27. Section Theme Matrix

| Section | Theme | Background |
|---------|-------|------------|
| Preloader | `theme_on-dark` | Dark |
| Hero | `theme_on-color` | Light/Color |
| Benefits Intro | `theme_on-brand` | Brand |
| Benefits | `theme_on-brand` | Brand |
| Quote | `theme_on-brand` | Brand |
| Location | `theme_on-brand` | Brand |
| Apartments | `theme_on-brand` | Brand |
| Amenities | `theme_on-color` | Light/Color |
| Interior | Default | Light |
| Architecture | `theme_on-color` | Light/Color |
| Other/FAQ | Default | Light |
| CTA | `theme_on-color` | Light/Color |
| Footer | `theme_on-dark` | Dark |
| Modals | `theme_on-dark` | Dark |
