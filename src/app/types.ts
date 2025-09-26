export interface Topic {
  term: string;
  category: string;
  score: number;
  percentChange: number;
  sparkline: number[];
  firstSeen: string;
  lastSeen: string;
  volume: number;
}

export interface FilterState {
  category: string;
  minScore: number;
  sortBy: 'score' | 'percentChange';
}

export interface SeedsData {
  categories: {
    [key: string]: {
      weight: number;
      terms: string[];
    };
  };
  globalSettings: {
    maxTopicsPerCategory: number;
    minVolumeThreshold: number;
    timeframe: string;
    geo: string;
    gprop: string;
  };
}
