import { Topic } from './types';

// Generate mock sparkline data
const generateSparkline = (trend: 'rising' | 'falling' | 'stable' = 'rising'): number[] => {
  const points = 24; // 24 weeks of data
  const data: number[] = [];
  
  for (let i = 0; i < points; i++) {
    let value = 50; // Base value
    
    if (trend === 'rising') {
      value += Math.random() * 20 + i * 2; // Rising trend
    } else if (trend === 'falling') {
      value += Math.random() * 20 - i * 1.5; // Falling trend
    } else {
      value += Math.random() * 30 + Math.sin(i * 0.3) * 10; // Stable with some variation
    }
    
    data.push(Math.max(0, Math.round(value)));
  }
  
  return data;
};

// Generate mock topics based on seeds data
export const mockTopics: Topic[] = [
  // AI Tools
  {
    term: "ChatGPT",
    category: "ai-tools",
    score: 8.7,
    percentChange: 245.3,
    sparkline: generateSparkline('rising'),
    firstSeen: "2023-01-15",
    lastSeen: "2024-01-15",
    volume: 85000
  },
  {
    term: "Claude",
    category: "ai-tools",
    score: 6.2,
    percentChange: 189.7,
    sparkline: generateSparkline('rising'),
    firstSeen: "2023-03-20",
    lastSeen: "2024-01-15",
    volume: 32000
  },
  {
    term: "Midjourney",
    category: "ai-tools",
    score: 5.8,
    percentChange: 156.2,
    sparkline: generateSparkline('rising'),
    firstSeen: "2022-11-10",
    lastSeen: "2024-01-15",
    volume: 28000
  },
  
  // E-commerce
  {
    term: "Dropshipping",
    category: "ecommerce",
    score: 4.3,
    percentChange: 78.9,
    sparkline: generateSparkline('stable'),
    firstSeen: "2023-06-01",
    lastSeen: "2024-01-15",
    volume: 45000
  },
  {
    term: "Print on Demand",
    category: "ecommerce",
    score: 3.9,
    percentChange: 92.4,
    sparkline: generateSparkline('rising'),
    firstSeen: "2023-04-15",
    lastSeen: "2024-01-15",
    volume: 22000
  },
  
  // Fitness
  {
    term: "Home Workout",
    category: "fitness",
    score: 7.1,
    percentChange: 134.6,
    sparkline: generateSparkline('rising'),
    firstSeen: "2023-02-01",
    lastSeen: "2024-01-15",
    volume: 67000
  },
  {
    term: "Yoga",
    category: "fitness",
    score: 2.8,
    percentChange: 45.2,
    sparkline: generateSparkline('stable'),
    firstSeen: "2023-08-10",
    lastSeen: "2024-01-15",
    volume: 18000
  },
  
  // Home Office
  {
    term: "Standing Desk",
    category: "home-office",
    score: 5.4,
    percentChange: 112.8,
    sparkline: generateSparkline('rising'),
    firstSeen: "2023-05-20",
    lastSeen: "2024-01-15",
    volume: 31000
  },
  {
    term: "Ergonomic Chair",
    category: "home-office",
    score: 4.7,
    percentChange: 89.3,
    sparkline: generateSparkline('rising'),
    firstSeen: "2023-07-05",
    lastSeen: "2024-01-15",
    volume: 25000
  },
  
  // Design Tools
  {
    term: "Figma",
    category: "design-tools",
    score: 6.9,
    percentChange: 167.4,
    sparkline: generateSparkline('rising'),
    firstSeen: "2023-01-30",
    lastSeen: "2024-01-15",
    volume: 52000
  },
  {
    term: "Canva",
    category: "design-tools",
    score: 3.2,
    percentChange: 56.7,
    sparkline: generateSparkline('stable'),
    firstSeen: "2023-09-12",
    lastSeen: "2024-01-15",
    volume: 19000
  },
  
  // Crypto
  {
    term: "Bitcoin",
    category: "crypto",
    score: 2.1,
    percentChange: -12.4,
    sparkline: generateSparkline('falling'),
    firstSeen: "2023-11-01",
    lastSeen: "2024-01-15",
    volume: 15000
  },
  {
    term: "NFT",
    category: "crypto",
    score: 1.8,
    percentChange: -28.9,
    sparkline: generateSparkline('falling'),
    firstSeen: "2023-10-15",
    lastSeen: "2024-01-15",
    volume: 12000
  },
  
  // Sustainability
  {
    term: "Solar Panels",
    category: "sustainability",
    score: 5.6,
    percentChange: 98.7,
    sparkline: generateSparkline('rising'),
    firstSeen: "2023-03-25",
    lastSeen: "2024-01-15",
    volume: 38000
  },
  {
    term: "Electric Vehicle",
    category: "sustainability",
    score: 4.9,
    percentChange: 123.5,
    sparkline: generateSparkline('rising'),
    firstSeen: "2023-02-14",
    lastSeen: "2024-01-15",
    volume: 29000
  }
];

export const categories = [
  "ai-tools",
  "ecommerce", 
  "fitness",
  "home-office",
  "design-tools",
  "crypto",
  "sustainability"
];
