import './App.css';
import { Box, Button, Typography, Select, MenuItem } from '@mui/material'
import { API } from 'aws-amplify';
import React, { useEffect } from 'react';
import { useState } from 'react';
import TableComponent from './TableComponent';
import axios from 'axios';


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
    const payload = {
      daysPerWeek: daysPerWeekOption,
      timePerSession: timePerSessionOption,
      fitnessGoal: fitnessGoalOption,
      userExperience: userExperienceOption,
      abs_bool: addAbs
    };
    const axios = require('axios');
    const headers = {
      // 'Access-Control-Allow-Origin': 'http://localhost:3000', // Replace with your frontend application's origin
      // 'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
      // 'Access-Control-Allow-Credentials': true,
      'Content-Type': 'application/json'
      };
    let config = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'https://zzswbozn7g.execute-api.us-east-1.amazonaws.com/production',
      headers: headers,
      // withCredentials: true,
    };

    axios.request(config)
    .then((response) => {
      console.log(JSON.stringify(response.data));
    })
    .catch((error) => {
      console.log(error);
    });

    //----------------------LAMBDA--------------------------------------
    // try { //Call the API using an amplify package and send 'payload'
    //   const response = await API.post('generateworkoutAPI', '/workout', {
    //     body: payload //If need to specify method, can send an 'httpMethod' header with payload
    //   });

    //   //Get status code from backend
    //   const status_check = response.statusCode

    //   // The backend outputs a dictionary, but stores it as a string by default.
    //   // The .parse function will convert it into an indexed list
    //   const data = JSON.parse(response.body);
      
    //   if (status_check === 400 || status_check === 500) {//400 error is unselected options for now, 500 is internal server error
    //     setExerciseData(data.body.replace(/"/g, ''));//Returns error w/o double quotes
    //   } else{ 
    //     //This command takes the indexed list (indexed by key for every value) and
    //     //Converts into an array so that the .map in TableComponent will work.
    //     const exerciseArray = Object.entries(data).map(([key, value]) => ({
    //       id: key,
    //       exercises: value,
    //     }));
    
        
    //     //Set the data to the array to pass later
    //     setExerciseData(exerciseArray);
    //   }   

    // } catch (error) {
    //   console.error(error);
    // };

    //--------------------------FLASK-----------------------------------------
    // For calling the flask app directly (local dev)
    // const url = 'http://127.0.0.1:5000/workout';
    // const url = 'https://zzswbozn7g.execute-api.us-east-1.amazonaws.com/production/entries';
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
    //     console.log(data)
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
    //     }


    //   })
    //   .catch((error) => {
    //     // Handle the error
    //     console.error(error);
    //   });


  };
  

  return (
    <div className="App">
      <Box sx={{ padding: 2 }}>
        <Typography variant="h1">
          Hi! Select the settings below and click the 'Generate Workout' button to get started!
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, marginBottom: 2 }}>
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
          <div>
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
        <TableComponent exerciseData={exerciseData} />
      </Box>
    </div>
  );
}

export default App;
