import React from 'react';
import { ResponsiveBar } from '@nivo/bar';
import { Box, useTheme } from '@mui/material';

const BarChart = ({ data }) => {
  const theme = useTheme();
  
  // Handle empty or invalid data
  if (!Array.isArray(data) || data.length === 0 || !data.some(series => Array.isArray(series.data) && series.data.length > 0)) {
    return (
      <Box 
        sx={{ 
          height: '100%', 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center',
          color: 'text.secondary',
          fontSize: '1.2rem'
        }}
      >
        No data available for chart
      </Box>
    );
  }

  // Transform data for the bar chart
  const transformedData = {};
  
  // First, collect all unique x values across all series
  const allXValues = new Set();
  data.forEach(series => {
    series.data.forEach(point => {
      if (point.x) allXValues.add(point.x);
    });
  });
  
  // Initialize objects for each x value
  allXValues.forEach(x => {
    transformedData[x] = { x };
  });
  
  // Fill in the y values for each series
  data.forEach(series => {
    series.data.forEach(point => {
      if (point.x && point.y !== undefined) {
        transformedData[point.x][series.id] = point.y;
      }
    });
  });
  
  // Convert to array
  const chartData = Object.values(transformedData);
  
  // Get keys (series names)
  const keys = data.map(series => series.id);
  
  // Generate colors
  const colors = {
    'Points': theme.palette.primary.main,
    'Rebounds': theme.palette.success.main,
    'Assists': theme.palette.info.main,
    // Add more colors for other potential series
  };

  return (
    <ResponsiveBar
      data={chartData}
      keys={keys}
      indexBy="x"
      margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
      padding={0.3}
      valueScale={{ type: 'linear' }}
      indexScale={{ type: 'band', round: true }}
      colors={({ id }) => colors[id] || theme.palette.secondary.main}
      borderColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
      axisTop={null}
      axisRight={null}
      axisBottom={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: 'Players',
        legendPosition: 'middle',
        legendOffset: 32
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: 'Value',
        legendPosition: 'middle',
        legendOffset: -40
      }}
      labelSkipWidth={12}
      labelSkipHeight={12}
      labelTextColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
      legends={[
        {
          dataFrom: 'keys',
          anchor: 'bottom-right',
          direction: 'column',
          justify: false,
          translateX: 120,
          translateY: 0,
          itemsSpacing: 2,
          itemWidth: 100,
          itemHeight: 20,
          itemDirection: 'left-to-right',
          itemOpacity: 0.85,
          symbolSize: 20,
          effects: [
            {
              on: 'hover',
              style: {
                itemOpacity: 1
              }
            }
          ]
        }
      ]}
      role="application"
      ariaLabel="NBA Stats Bar Chart"
      barAriaLabel={e => `${e.id}: ${e.formattedValue} for ${e.indexValue}`}
      theme={{
        axis: {
          ticks: {
            text: {
              fill: theme.palette.text.secondary,
            }
          },
          legend: {
            text: {
              fill: theme.palette.text.primary,
              fontSize: 12
            }
          }
        },
        legends: {
          text: {
            fill: theme.palette.text.primary,
          }
        },
        tooltip: {
          container: {
            background: theme.palette.background.paper,
            color: theme.palette.text.primary,
            fontSize: 12,
            borderRadius: 4,
            boxShadow: theme.shadows[3],
          }
        }
      }}
      animate={true}
      motionStiffness={90}
      motionDamping={15}
    />
  );
};

export default BarChart; 