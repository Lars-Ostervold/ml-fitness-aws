import React from 'react';
import { Typography } from '@mui/material';

const TableComponent = ({ exerciseData }) => {
  if (typeof exerciseData === 'string') { //Check if String, which means backend failed
    return <Typography variant="h3">{exerciseData}</Typography>;
  }
  
  return (
    <div>
      {exerciseData.map(({ id, exercises }) => (
        <div key={id}>
          <Typography variant="h3">{getDayOfWeek(id)}</Typography>
          <ul style={{ listStyle: 'none'}}>
            {exercises.map((exercise, index) => (
              <li key={index}>{exercise}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

// Helper function to get the day of the week based on index
const getDayOfWeek = (index) => {
  const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  return daysOfWeek[index] || '';
};

export default TableComponent;

