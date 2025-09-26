interface SparklineProps {
  data: number[];
  width?: number;
  height?: number;
  className?: string;
}

export default function Sparkline({ 
  data, 
  width = 100, 
  height = 30, 
  className = "" 
}: SparklineProps) {
  if (!data || data.length === 0) {
    return (
      <div 
        className={`bg-gray-100 dark:bg-gray-800 rounded ${className}`}
        style={{ width, height }}
      />
    );
  }

  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;

  const points = data.map((value, index) => {
    const x = (index / (data.length - 1)) * width;
    const y = height - ((value - min) / range) * height;
    return `${x},${y}`;
  }).join(' ');

  const pathData = `M ${points}`;

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      className={className}
    >
      <path
        d={pathData}
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="text-blue-500"
      />
    </svg>
  );
}
