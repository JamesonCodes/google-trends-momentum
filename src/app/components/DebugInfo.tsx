'use client';

import { Topic } from '../types';

interface DebugInfoProps {
  topics: Topic[];
  lastUpdated: string | null;
  loading: boolean;
  error: string | null;
  refreshKey: number;
}

export default function DebugInfo({ topics, lastUpdated, loading, error, refreshKey }: DebugInfoProps) {
  if (process.env.NODE_ENV !== 'development') {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 bg-black bg-opacity-80 text-white p-4 rounded-lg text-xs max-w-sm">
      <h4 className="font-bold mb-2">Debug Info</h4>
      <div>Topics: {topics.length}</div>
      <div>Last Updated: {lastUpdated || 'Never'}</div>
      <div>Loading: {loading ? 'Yes' : 'No'}</div>
      <div>Error: {error || 'None'}</div>
      <div>Refresh Key: {refreshKey}</div>
      <div>First Topic: {topics[0]?.term || 'None'}</div>
    </div>
  );
}
