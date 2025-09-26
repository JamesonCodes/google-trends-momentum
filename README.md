# Rising Topics

A modern web application for discovering trending and rising topics across various categories. Built with Next.js 14, TypeScript, and powered by real-time Google Trends data.

## Features

- **Real-time Data**: Live trending topics from Google Trends API
- **Professional UI**: Clean, modern interface with interactive charts
- **Smart Filtering**: Filter by category, time period, and trend status
- **Trend Analysis**: Visual sparklines and growth metrics
- **Auto-refresh**: Automatic data updates with manual refresh capability
- **Responsive Design**: Works perfectly on all devices

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Data Pipeline**: Python, pytrends, pandas, numpy
- **Charts**: Custom SVG sparklines
- **Deployment**: Vercel-ready

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Testing

Run the test suite:

```bash
# Run all tests
npm run test

# Run MVP functionality tests only
npm run test:mvp

# Run specific test
python tests/test_mvp_functionality.py
```

## Project Structure

```
rising-topics/
├── src/app/           # Next.js app directory
├── scripts/           # Build and utility scripts
├── tests/             # Test suite
├── public/data/       # Generated data files
└── data/              # Seed data and configuration
```

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
