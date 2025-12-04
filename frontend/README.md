# AI SaaS Frontend - Next.js 14

Ultra-minimal black & white frontend for the AI SaaS boilerplate.

## 🎨 Design

- **Colors**: Pure black (#000000) background, white (#ffffff) text
- **Style**: Glassmorphism effects, minimal borders
- **Animations**: Buttery smooth spring physics with Framer Motion
- **Inspiration**: Claude.ai / Perplexity aesthetic

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

Open [http://localhost:3000](http://localhost:3000)

## 📦 Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Notifications**: Sonner
- **State**: Zustand
- **HTTP**: Axios

## 📁 Project Structure

```
src/
├── app/
│   ├── (protected)/          # Protected routes
│   │   ├── dashboard/        # Dashboard page
│   │   └── layout.tsx        # Protected layout with auth check
│   ├── login/                # Login page
│   ├── register/             # Register page
│   ├── forgot-password/      # Password reset page
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Home (redirects)
│   └── globals.css           # Global styles
├── components/
│   ├── ui/                   # shadcn/ui components
│   └── page-transition.tsx   # Page transition wrapper
├── lib/
│   ├── api.ts                # API client with interceptors
│   └── utils.ts              # Utility functions
└── store/
    └── auth.ts               # Auth state management
```

## 🔐 Authentication Flow

1. User visits `/` → redirects to `/login` or `/dashboard`
2. Login/Register → stores JWT tokens in localStorage
3. Protected routes check auth status
4. Auto token refresh on 401 errors
5. Logout clears tokens and redirects to login

## 🎯 Features

### Milestone 1 (Current)
- ✅ Global layout with smooth transitions
- ✅ Login, Register, Forgot Password pages
- ✅ Protected routes with auth check
- ✅ Session management
- ✅ Dark mode only
- ✅ Glassmorphism effects
- ✅ Mobile responsive
- ✅ Spring physics animations

### Upcoming
- [ ] Dashboard with real data
- [ ] Organization management
- [ ] Billing & subscriptions
- [ ] AI chat interface
- [ ] Settings page
- [ ] Profile management

## 🎨 Design System

### Colors
```css
background: #000000
foreground: #ffffff
card: #1a1a1a
border: #2a2a2a
muted: #a0a0a0
```

### Typography
- **Font**: Inter (sans-serif)
- **Mono**: Geist Mono

### Animations
All animations use spring physics:
```typescript
transition={{
  type: "spring",
  stiffness: 260,
  damping: 20,
}}
```

## 🔧 Configuration

### Environment Variables

Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`.

Make sure the backend is running before starting the frontend.

## 📱 Responsive Design

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

All components are fully responsive with mobile-first approach.

## 🚢 Deployment

### Vercel (Recommended)
```bash
vercel deploy
```

### Docker
```bash
docker build -t ai-saas-frontend .
docker run -p 3000:3000 ai-saas-frontend
```

### Environment Variables for Production
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

## 🧪 Testing

```bash
# Run linter
npm run lint

# Type check
npx tsc --noEmit
```

## 📝 License

MIT
