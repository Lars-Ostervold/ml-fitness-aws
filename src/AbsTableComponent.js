import React, { useState } from 'react';
import { Typography, Button } from '@mui/material';
import Paper from '@mui/material/Paper';
import './TableComponent.css';

const AbsTableComponent = ({ exerciseData, absExercises }) => {
  //This creates a reference to same memory location as exerciseData
  //Therefore, when updatedExerciseData is updated, exerciseData is updated
  //So we adjust this variable, and the table will update
  const [updatedExerciseData, setUpdatedExerciseData] = useState([]);


  //This function takes the name of the exercise, send it to the backend, and
  //returns a new exercise
  const handleRerollExercise = (exercise, dayIndex, exerciseIndex) => {
    const payload = {
      'exercise': exercise
    };
    const headers = {
      'Content-Type': 'application/json'
      };

    // --------------------------AWS-----------------------------------------
    const axios = require('axios');
    const url = 'https://x4xecbx769.execute-api.us-east-1.amazonaws.com/default/reroll_workout';

    axios.post(url, payload, { headers })
      .then(response => {
        const data = response.data;       
        const newExercise = JSON.parse(data.body)
        const updatedExercises = [...exerciseData] //Copy of exerciseData
        updatedExercises[dayIndex].exercises[exerciseIndex] = newExercise
        setUpdatedExerciseData(updatedExercises)
      })

    // --------------------------AWS-----------------------------------------


    // --------------------------FLASK-----------------------------------------
    // const url = 'http://127.0.0.1:5000/reroll';
    // const headers = {'Content-Type': 'application/json'};
    // const body = JSON.stringify({ payload });
    // fetch(url, {
    //   method: 'POST',
    //   headers: headers,
    //   body: body
    // })
    //   .then((response) => response.json()) 
    //   .then((data) => { 
    //     const newExercise = JSON.parse(data.body)
    //     const updatedExercises = [...exerciseData] //Copy of exerciseData
    //     updatedExercises[dayIndex].exercises[exerciseIndex] = newExercise
    //     setUpdatedExerciseData(updatedExercises)
        
    //   })
    //--------------------------FLASK-----------------------------------------
      .catch((error) => {
        // Handle the error
        console.error(error);
      });
  };

  
  if (typeof exerciseData === 'string') {
    // Check if String, which means backend failed
    return <Typography variant="h3">{exerciseData}</Typography>;
  }

  return (
    <div className="container">
      {exerciseData.map(({ id, exercises }, dayIndex) => (
        <div key={id} className="table-container">
          <div className="table-column">
            <Typography variant="h3">{getDayOfWeek(id)}</Typography>
            <Paper elevation={3} className="centered-paper">
              <table>
                <thead>
                  <tr>
                    <th>Exercise</th>
                    <th>Sets</th>
                    <th>Reps</th>
                    <th>Reroll</th>
                  </tr>
                </thead>
                <tbody>
                  {exercises.map((exercise, exerciseIndex) => (
                    <tr key={exerciseIndex}>
                      <td>{exercise[0]}</td>
                      <td>{exercise[1]}</td>
                      <td>{exercise[2]}</td>
                      <td>
                        <Button variant="outlined" onClick={() => handleRerollExercise(exercise, dayIndex, exerciseIndex)}>
                          Reroll
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Paper>
          </div>
          <div className="table-column">
            <Paper elevation={3} className="centered-paper">
              <table>
                <thead>
                  <tr>
                    <th>Ab Routine 2 cycles, 45 seconds on, 15 second break</th>
                  </tr>
                </thead>
                <tbody>
                  {absExercises[id]?.map((exercise, index) => (
                    <tr key={index}>
                      <td>{exercise}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Paper>
          </div>
        </div>
      ))}
    </div>
  );
};

// Rest of the code remains the same


// Helper function to get the day of the week based on index
const getDayOfWeek = (index) => {
  const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  return daysOfWeek[index] || '';
};

export default AbsTableComponent;
