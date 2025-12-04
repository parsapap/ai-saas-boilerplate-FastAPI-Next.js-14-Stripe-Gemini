# Dashboard Documentation

## Overview
A premium, production-ready dashboard with smooth animations, glassmorphism effects, and a minimal black & white theme.

## Features

### 🎨 Design
- **Minimal Black & White Theme**: Clean, professional aesthetic
- **Glassmorphism**: Frosted glass effect on all cards
- **Smooth Animations**: Framer Motion throughout
- **Responsive**: Mobile-first design with collapsible sidebar

### 📊 Components

#### Sidebar
- Collapsible on mobile with smooth slide animation
- Active state highlighting with white background
- Menu items with icons
- Bottom upgrade card
- Responsive with backdrop blur

#### Top Bar
- Organization switcher dropdown
- User info display
- Logout button
- Responsive layout

#### Dashboard Cards
1. **Stats Cards**: Show key metrics with trends
2. **Usage Chart**: Circular progress showing quota
3. **Activity Chart**: Line chart for 7-day usage
4. **Recent Chats**: List of conversations with timestamps

#### Floating Action Button
- Bottom-right positioned
- Subtle pulse animation
- Smooth hover/tap effects
- Creates new chat

### ✨ Animations

All animations use Framer Motion for smooth, premium feel:

```typescript
// Entrance Animation
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.5 }}

// Hover Lift
whileHover={{ y: -4, transition: { duration: 0.2 } }}

// Stagger Effect
transition={{ delay: index * 0.1 }}
```

### 🎯 Key Design Patterns

#### Glassmorphism
```typescript
className="bg-white/5 backdrop-blur-xl border border-white/10"
```

#### Hover Effects
```typescript
className="hover:bg-white/10 hover:border-white/20 transition-all duration-300"
```

#### Card Lift
```typescript
whileHover={{ y: -4, transition: { duration: 0.2 } }}
```

## Usage

### Basic Dashboard
```typescript
import { DashboardPage } from "@/app/(protected)/dashboard/page";

export default function Page() {
  return <DashboardPage />;
}
```

### Stats Card
```typescript
import { StatsCard } from "@/components/dashboard/stats-card";
import { MessageSquare } from "lucide-react";

<StatsCard
  title="Total Messages"
  value="125"
  icon={MessageSquare}
  trend={{ value: 12, isPositive: true }}
  delay={0.1}
/>
```

### Usage Chart
```typescript
import { UsageChart } from "@/components/usage-chart";

<UsageChart used={125} limit={1000} />
```

### Empty State
```typescript
import { EmptyState } from "@/components/dashboard/empty-state";
import { MessageSquare } from "lucide-react";

<EmptyState
  icon={MessageSquare}
  title="No chats yet"
  description="Start a conversation to see it here"
  action={{
    label: "New Chat",
    onClick: () => console.log("Create chat")
  }}
/>
```

## Customization

### Colors
The theme uses white with opacity for all elements:
- `white/5`: Background
- `white/10`: Borders
- `white/20`: Hover borders
- `white/40`: Secondary text
- `white/60`: Muted text

### Animation Timings
- Entrance: 0.5s
- Hover: 0.2s
- Transitions: 0.3s
- Stagger: 0.1s per item

### Responsive Breakpoints
- Mobile: < 768px (sidebar collapses)
- Tablet: 768px - 1024px (2-column grid)
- Desktop: > 1024px (full layout)

## Performance

### Optimizations
1. **Lazy Loading**: Components load on demand
2. **Skeleton States**: Smooth loading experience
3. **Memoization**: Prevent unnecessary re-renders
4. **CSS Transitions**: Hardware-accelerated animations

### Bundle Size
- Recharts: ~50KB gzipped
- Framer Motion: ~30KB gzipped
- Lucide Icons: ~5KB gzipped (tree-shaken)

## Accessibility

- Semantic HTML elements
- ARIA labels on interactive elements
- Keyboard navigation support
- Focus visible states
- Screen reader friendly

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari, Chrome Android

## Future Enhancements

- [ ] Real-time data updates
- [ ] Dark/light mode toggle
- [ ] Customizable dashboard layout
- [ ] Export data functionality
- [ ] Advanced filtering
- [ ] More chart types

## Troubleshooting

### Animations not working
Ensure Framer Motion is installed:
```bash
npm install framer-motion
```

### Charts not rendering
Check Recharts installation:
```bash
npm install recharts
```

### Icons missing
Install Lucide React:
```bash
npm install lucide-react
```

## License
MIT
