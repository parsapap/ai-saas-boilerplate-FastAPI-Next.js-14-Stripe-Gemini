# Frontend Setup Guide

## Prerequisites

- Node.js 18+ installed
- Backend running on `http://localhost:8000`

## Installation Steps

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Download Fonts (Optional)

Download Geist Mono font from [Vercel Font](https://vercel.com/font) and place `GeistMonoVF.woff` in `src/app/fonts/`

Or the app will fallback to system monospace fonts.

### 4. Start Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## First Time Setup

1. **Start Backend First**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test the Flow**
   - Visit `http://localhost:3000`
   - Click "Sign up" to create an account
   - Fill in the registration form
   - You'll be redirected to the dashboard

## Troubleshooting

### CORS Errors

Make sure your backend `.env` has:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### API Connection Failed

1. Check backend is running: `curl http://localhost:8000/health`
2. Check `.env.local` has correct API URL
3. Check browser console for errors

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run dev
```

## Production Build

```bash
# Build
npm run build

# Test production build locally
npm start
```

## Features Checklist

- ✅ Login page with glassmorphism
- ✅ Register page with validation
- ✅ Forgot password page
- ✅ Protected dashboard
- ✅ Smooth page transitions
- ✅ Mobile responsive
- ✅ Auto token refresh
- ✅ Session management

## Next Steps

1. Customize the dashboard with real data
2. Add more protected pages (settings, profile, etc.)
3. Integrate Stripe billing UI
4. Add AI chat interface
5. Deploy to Vercel

## Support

For issues, check:
- Backend logs: `docker-compose logs backend`
- Frontend console: Browser DevTools
- Network tab: Check API calls

Happy coding! 🚀
