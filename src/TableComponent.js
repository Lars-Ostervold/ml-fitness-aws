import React from 'react';

const TableComponent = ({ exerciseData }) => {
  // console.log('Table component - Type is exerciseData type:', typeof exerciseData)
  // console.log('Table component - This is exerciseData printout:')
  // console.log(exerciseData)
  // if (!Array.isArray(exerciseData)) {
  //   // Display an error message or return null if exerciseData is not an array
  //   return <p>Error: Invalid exercise data</p>;
  // }

  return (
    <div>
      {exerciseData.map(({ id, exercises }) => (
        <div key={id}>
          <h3>Group {id}</h3>
          <ul>
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
  const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
  return daysOfWeek[index] || '';
};

export default TableComponent;

