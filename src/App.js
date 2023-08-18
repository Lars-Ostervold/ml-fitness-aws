import './App.css';
import { Box, Button, Typography, Select, MenuItem } from '@mui/material'
import React, { useEffect } from 'react';
import { useState } from 'react';
import TableComponent from './TableComponent';
import AbsTableComponent from './AbsTableComponent';
import axios from 'axios';

console.log('have good day')

function App() {
  const [daysPerWeekOption, setdaysPerWeekOption] = useState('');
  const [timePerSessionOption, settimePerSessionOption] = useState('');
  const [fitnessGoalOption, setfitnessGoalOption] = useState('');
  const [userExperienceOption, setuserExperienceOption] = useState('');
  const [addAbs, setAddAbs] = useState(false);
  const [exerciseData, setExerciseData] = useState([]);
  const [availableDaysPerWeekOptions, setAvailableDaysPerWeekOptions] = useState([
    "1", "2", "3", "4", "5", "6", "7"
  ]);
  const [absExercises, setAbsExercises] = useState([]);
  const [tempAbsExercises, setTempAbsExercises] = useState([]);

  
  const handleUserExperienceChange = (e) => {
    const selectedValue = e.target.value;
    setuserExperienceOption(selectedValue);
  
    // Update the available options for "Days per Week" based on the selected value
    if (selectedValue === "1") {
      setAvailableDaysPerWeekOptions(["1", "2", "3"]);
    } else if (selectedValue === "2") {
      setAvailableDaysPerWeekOptions(["2", "3", "4", "5"]);
    } else {
      setAvailableDaysPerWeekOptions(["2", "3", "4", "5", "6", "7"]);
    }
  };
  

  const handleSubmit = async () => {
    
    //Clear the temporary list. It gets replenished each new run and then we set the absExercises to the temp list
    setTempAbsExercises([]);


    const payload = {
      daysPerWeek: daysPerWeekOption,
      timePerSession: timePerSessionOption,
      fitnessGoal: fitnessGoalOption,
      userExperience: userExperienceOption,
      abs_bool: addAbs
    };
    
    
  // --------------------------AWS-----------------------------------------
  // // Call the API using an axios package and send 'payload'
  const axios = require('axios');
  const headers = {
    'Content-Type': 'application/json'
    };

  const url = 'https://zzswbozn7g.execute-api.us-east-1.amazonaws.com/production';

  axios.post(url, payload, { headers })
    .then(response => {
      const data = response.data;
      const status_check = data.statusCode;
      const data2 = JSON.parse(data.body);
      
      if (status_check === 400 || status_check === 500) {
        setExerciseData(data.body.replace(/"/g, ''));
      } else { 
        const exerciseArray = Object.entries(data2).map(([key, value]) => ({
          id: key,
          exercises: value,
        }));

        setExerciseData(exerciseArray);
      
          if (addAbs === true){
            for (var i = 0; i < exerciseArray.length; i++){
              var day = exerciseArray[i].exercises
              var lastExercise = day[day.length - 1]
              tempAbsExercises.push(lastExercise)
              day.pop()
            }
          }
        }
        setAbsExercises(tempAbsExercises)
      
    })

    //--------------------------FLASK-----------------------------------------
    // For calling the flask app directly (local dev)
    // const url = 'http://127.0.0.1:5000/workout';
    // const headers = {'Content-Type': 'application/json'};
    // const body = JSON.stringify({ payload });
    // fetch(url, {
    //   method: 'POST',
    //   headers: headers,
    //   body: body
    // })
    //   .then((response) => response.json()) 
      
    //   // Parse the response as JSON
    //   //With fetch, response.body can't be called directly, so we parse response
    //   //with response.json() first, then reponse gets stored as whatever we call
    //   //in the next arrow function (data in this case), which we can then access
    //   //body with data.body
    //   .then((data) => { 
    //     const status_check = data.statusCode //Get status code from backend
    //     const data2 = JSON.parse(data.body)
        
    //     if (status_check === 400 || status_check === 500) {//400 error is unselected options for now, 500 is internal server error
    //       setExerciseData(data.body.replace(/"/g, ''));//Returns error w/o double quotes
    //     } else{ 
    //       const exerciseArray = Object.entries(data2).map(([key, value]) => ({
    //         id: key,
    //         exercises: value,
    //       }));
      
    //       setExerciseData(exerciseArray);

    //       //If abs is selected, get the last exercise of each day and store in absExercises
    //       //Also, we need to remove these exercises from the exerciseArray so they don't get printed twice
    //       if (addAbs === true){
    //         for (var i = 0; i < exerciseArray.length; i++){
    //           var day = exerciseArray[i].exercises
    //           var lastExercise = day[day.length - 1]
    //           tempAbsExercises.push(lastExercise)
    //           day.pop()
    //         }
    //       }
    //     }
    //     setAbsExercises(tempAbsExercises)
    //--------------------------END FLASK-----------------------------------------

    //   })
      .catch((error) => {
        // Handle the error
        console.error(error);
      });
  

  };
  

  return (
    <div className="App">
      <Box sx={{ padding: 2 }}>
        <Typography variant="h1">
          Hi! Select the settings below and click the 'Generate Workout' button to get started!
        </Typography>

      <Box className='selectBoxContainer'>
        <div>
          <Select
            name="userExperience"
            value={userExperienceOption}
            onChange={handleUserExperienceChange}
          >
            <MenuItem value="1">Beginner</MenuItem>
            <MenuItem value="2">Intermediate</MenuItem>
            <MenuItem value="3">Advanced</MenuItem>
          </Select>
          <Typography variant="h6">Gym Experience</Typography>
        </div>
        <div>
          <Select
            name="daysPerWeek"
            value={daysPerWeekOption}
            onChange={(e) => setdaysPerWeekOption(e.target.value)}
          >
            {availableDaysPerWeekOptions.map((option) => (
              <MenuItem key={option} value={option}>
                {option}
              </MenuItem>
            ))}
          </Select>
          <Typography variant="h6">Days per Week</Typography>
        </div>
        <div>
          <Select
            name="timePerSession"
            value={timePerSessionOption}
            onChange={(e) => settimePerSessionOption(e.target.value)}
          >
            <MenuItem value="15">15</MenuItem>
            <MenuItem value="30">30</MenuItem>
            <MenuItem value="45">45</MenuItem>
            <MenuItem value="60">60</MenuItem>
          </Select>
          <Typography variant="h6">Time per Session</Typography>
        </div>
        <div>
          <Select
            name="fitnessGoal"
            value={fitnessGoalOption}
            onChange={(e) => setfitnessGoalOption(e.target.value)}
          >
            <MenuItem value="1">Strength</MenuItem>
            <MenuItem value="2">Body Building</MenuItem>
            <MenuItem value="3">Lean</MenuItem>
          </Select>
          <Typography variant="h6">Fitness Goal</Typography>
        </div>
        <div className='checkboxContainer'>
          <label htmlFor="addAbsCheckbox">
            <input
              type="checkbox"
              id="addAbsCheckbox"
              checked={addAbs}
              onChange={(e) => setAddAbs(e.target.checked)}
            />
            Add 5-10 minutes of abs?
          </label>
        </div>

      </Box>
        <Button variant="contained" onClick={handleSubmit}>
          Generate Workout
        </Button>
      </Box>
      <Box sx={{ padding: 2 }}>
        <div className="tables-container">
          
          {/* if addAbs, call AbsTableComponent, otherwise call exerciseData */}
          {addAbs && absExercises.length > 0 ? (
            <div className="abs-table">
              <AbsTableComponent exerciseData = {exerciseData} absExercises={absExercises} />
            </div>
          ) : (
            <div className="main-table">
              <TableComponent exerciseData={exerciseData} />
            </div>
          )}
        </div>
        
      </Box>
    </div>
  );
}

export default App;
