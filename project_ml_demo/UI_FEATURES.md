# 🎨 UI Features Guide

## Color Palette

### Primary Colors:
- **Cyan Blue**: `#00F5FF` - Main accent color
- **Deep Blue**: `#00D4FF` - Secondary accent
- **Purple Gradient**: `#667eea` to `#764ba2` - Buttons
- **Dark Background**: `#0F2027` to `#2C5364` - Animated gradient

### Status Colors:
- **Success/High**: `#4CAF50` (Green)
- **Warning/Medium**: `#FFC107` (Amber)
- **Error/Low**: `#FF5252` (Red)

## Key Features

### 🌊 Animated Background
The main background features a smooth gradient animation that shifts between dark blue tones, creating a dynamic and modern feel.

### ✨ Gradient Text
All major headings use animated gradient text that shifts through various shades of cyan and blue.

### 💳 Card Design
All cards feature:
- Semi-transparent backgrounds with blur effect (glassmorphism)
- Glowing borders matching the accent colors
- Hover animations that lift the card
- Smooth box shadows

### 🎯 Score Display
The prediction score features:
- **Large, bold number** (4rem font size)
- **Dynamic color coding**:
  - Green for scores ≥ 8
  - Yellow for scores 5-7.99
  - Red for scores < 5
- **Progress bar** showing score out of 10
- **Glowing text shadow** matching the score color

### 📊 Charts
All Plotly charts are customized with:
- Dark transparent backgrounds
- Cyan accent colors
- Custom grid colors
- Smooth animations

### 📱 Responsive Breakpoints

#### Desktop (> 768px)
- Full-size fonts
- Wide layout
- All features visible

#### Tablet (480px - 768px)
- Font sizes reduced by ~20%
- Adjusted padding
- Optimized button sizes

#### Mobile (< 480px)
- Font sizes reduced by ~30%
- Compact tab layout
- Single column layout
- Touch-optimized controls

## Icon Usage

### Sidebar Icons:
- 🎓 Dashboard header
- ⏰ Study hours
- ✅ Attendance
- 📋 Assignment completion
- 💻 Internet use
- 🔥 Motivation
- 👨‍👩‍👧 Family support
- 😰 Stress level
- 💼 Part-time hours

### Tab Icons:
- 📈 Prediction & Analysis
- 📊 Data Exploration
- ⚙️ Model Performance

### Metric Icons:
- 📝 Total samples
- 📊 Input variables
- 📈 Average score
- 🎯 Highest score

## Animation Details

### Fade In (1s)
Applied to main content on page load

### Gradient Shift (15s loop)
Background gradient animation

### Hover Effects (0.3s)
- Cards lift up 5px
- Buttons lift up 2px
- Box shadow intensifies
- Border colors brighten

### Pulse Effect (0.5s)
Applied to buttons on hover

## Typography

### Font Family: Poppins
- **Light (300)**: Body text
- **Regular (400)**: Standard text
- **SemiBold (600)**: Headings
- **Bold (700)**: Main titles

### Font Sizes (Desktop):
- **H1**: 3rem (48px)
- **H2**: 1.5rem (24px)
- **H3**: 1.25rem (20px)
- **Body**: 1rem (16px)
- **Score Display**: 4rem (64px)

## Best Practices for Viewing

### Recommended Browsers:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari

### Optimal Screen Sizes:
- **Desktop**: 1920x1080 or higher
- **Tablet**: 1024x768 or similar
- **Mobile**: 375x667 (iPhone) or 360x640 (Android)

### Performance Tips:
- Use hardware acceleration in browser
- Close unnecessary tabs for smooth animations
- Ensure good internet connection for Google Fonts

## Accessibility

- High contrast ratios for readability
- Clear visual hierarchy
- Touch-friendly button sizes (minimum 44x44px)
- Readable font sizes even on mobile
- Color coding supplemented with text labels
- Hover states for all interactive elements

## Future Enhancement Ideas

- Dark/Light mode toggle
- Custom color theme selector
- More animation options
- Interactive tutorials
- Export functionality with styled reports
- Multi-language support with flag icons
