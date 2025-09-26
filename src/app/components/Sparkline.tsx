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

  // Add padding to the chart
  const padding = 4;
  const chartWidth = width - (padding * 2);
  const chartHeight = height - (padding * 2);

  const points = data.map((value, index) => {
    const x = padding + (index / (data.length - 1)) * chartWidth;
    const y = padding + chartHeight - ((value - min) / range) * chartHeight;
    return `${x},${y}`;
  });

  const pathData = `M ${points.join(' L ')}`;

  // Create area fill
  const areaData = `${pathData} L ${points[points.length - 1].split(',')[0]},${padding + chartHeight} L ${points[0].split(',')[0]},${padding + chartHeight} Z`;

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      className={className}
    >
      {/* Gradient definition */}
      <defs>
        <linearGradient id="sparklineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="currentColor" stopOpacity="0.3" />
          <stop offset="100%" stopColor="currentColor" stopOpacity="0.05" />
        </linearGradient>
      </defs>
      
      {/* Area fill */}
      <path
        d={areaData}
        fill="url(#sparklineGradient)"
        className="text-blue-500"
      />
      
      {/* Line */}
      <path
        d={pathData}
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="text-blue-600"
      />
      
      {/* Data points */}
      {points.map((point, index) => {
        const [x, y] = point.split(',').map(Number);
        return (
          <circle
            key={index}
            cx={x}
            cy={y}
            r="1.5"
            fill="currentColor"
            className="text-blue-600"
          />
        );
      })}
    </svg>
  );
}
