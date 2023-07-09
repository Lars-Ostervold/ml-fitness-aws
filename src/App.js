import logo from './logo.svg';
import './App.css';
import { API } from 'aws-amplify';
import React, { useEffect } from 'react';
import { useState } from 'react';
import TableComponent from './TableComponent';
// import { Lambda } from 'aws-sdk';


function App() {
  const [selectedOption1, setSelectedOption1] = useState('');
  const [selectedOption2, setSelectedOption2] = useState('');
  const [selectedOption3, setSelectedOption3] = useState('');
  const [selectedOption4, setSelectedOption4] = useState('');
  const [exerciseData, setExerciseData] = useState([]);

  // const handleSubmit = async () => {
  //   const lambda = new Lambda({ region: 'us-east-1' }); // Update the region as per your Lambda function's region
  
  //   const payload = {
  //     option1: selectedOption1,
  //     option2: selectedOption2,
  //     option3: selectedOption3,
  //     option4: selectedOption4
  //   };
  
  //   const params = {
  //     FunctionName: 'YourLambdaFunctionName',
  //     Payload: JSON.stringify(payload)
  //   };
  
  //   try {
  //     const response = await lambda.invoke(params).promise();
  //     const data = JSON.parse(response.Payload);
  //     console.log(data);
  //     setExerciseData(data); // Example: Assuming the response is JSON data
  //     console.log('Here is the exercise data:');
  //     console.log(exerciseData);
  //   } catch (error) {
  //     console.error(error);
  //   }
  // };


  const handleSubmit = async () => {
    const payload = {
      option1: selectedOption1,
      option2: selectedOption2,
      option3: selectedOption3,
      option4: selectedOption4
    };
    
    // const url = 'https://dy9s1q0nb8.execute-api.us-east-1.amazonaws.com/dev/workout'
    // const headers = {'Content-Type': 'application/json'};
    // const body = JSON.stringify({ payload });

    try {
      const response = await API.post('generateworkoutAPI', '/workout', {
        body: payload
      });
      // console.log('This is type of response:', typeof response)
      // console.log(response)
      // console.log('This is response.body:')
      // console.log(response.body)
      // console.log('this is type of body:', typeof response.body)


      const data = JSON.parse(response.body);
      console.log(data)

      const exerciseArray = Object.entries(data).map(([key, value]) => ({
        id: key,
        exercises: value,
      }));
      console.log(exerciseArray);

      setExerciseData(exerciseArray);
      console.log(exerciseData)
    } catch (error) {
      console.error(error);
    };

    // For calling the flask app directly
    //const url = 'http://127.0.0.1:5000/workout'; //for local dev
    // fetch(url, {
    //   method: 'POST',
    //   headers: headers,
    //   body: body
    // })
    //   .then((response) => response.json())
    //   .then((data) => {
    //     console.log(data)
    //     setExerciseData(data); // Example: Assuming the response is JSON data
    //     console.log('Here is the excercise data:')
    //     console.log(exerciseData)
    //   })
    //   .then((sortedList) => {
    //     // Handle the sorted list response
    //   })
    //   .catch((error) => {
    //     // Handle the error
    //     console.error(error);
    //   });

    // await API.post("generateworkoutAPI", "/workout", {'Content-Type': 'application/json', 'Accept': 'application/json', data} )
    //   .then((response) => {
    //     // Handle the response from the backend
    //     console.log(response)
    //     setExerciseData(response.data); // Example: Assuming the response is JSON data
    //     console.log('Here is the excercise data:')
    //     console.log(exerciseData)
    //   })
    //   .catch((error) => {
    //     // Handle any error that occurs during the API request
    //     console.error(error);
    //   });
  };
  

  return (
    <div className="App">
      <div className="welcome-message">
        <h1>Hi! Select the settings below and click the 'Generate Workout' button to get started!</h1>
      </div>
      <div className="dropdowns">
        <select name="option1" value={selectedOption1} onChange={(e) => setSelectedOption1(e.target.value)}>
          <option value="">Days per week</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
          <option value="6">6</option>
          <option value="7">7</option>
          {/* Add more options as needed */}
        </select>
        <select name="option2" value={selectedOption2} onChange={(e) => setSelectedOption2(e.target.value)}>
          <option value="">Time per Session</option>
          <option value="15">15</option>
          <option value="30">30</option>
          <option value="45">45</option>
          <option value="60">60</option>
          {/* Add more options as needed */}
        </select>
        <select name="option3" value={selectedOption3} onChange={(e) => setSelectedOption3(e.target.value)}>
          <option value="">Fitness Goal</option>
          <option value="1">Strength</option>
          <option value="2">Body Building</option>
          <option value="3">Lean</option>
          {/* Add more options as needed */}
        </select>
        <select name="option4" value={selectedOption4} onChange={(e) => setSelectedOption4(e.target.value)}>
          <option value="">Gym Experience</option>
          <option value="1">Beginner</option>
          <option value="2">Intermediate</option>
          <option value="3">Expert</option>
          {/* Add more options as needed */}
        </select>
      </div>

      <button className="submit-button" onClick={handleSubmit}>
        Generate Workout
      </button>
    

      <TableComponent exerciseData={exerciseData} />

    </div>
  );
}

export default App;
