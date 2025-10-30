import './App.css';
import { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Headline[]>([]);

  const backendURL = window.location.hostname === 'localhost'
      ? 'http://127.0.0.1:8000'
      : 'https://financenewssetiment.onrender.com'

  const predict = async() => {
    try{
      const response = await axios.post(`${backendURL}/predict`,{
        brand: query
      })
      setResults([...response.data.headlines]);
      console.log(response.data)
    }
    catch(error){
      return(error)
    }
  }

  interface Headline {
    text: string;
    prediction: string;
  }

  return (
    <div className="App">
      <div className='App-header'>
        <h1>News setiment analyzer</h1>
      </div>

      <div className='searchSection'>
        <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Enter company or topic..." />
        <button onClick={predict}>Analyze</button>
      </div>
      

      <ul className='listSection'>
        {results.map((item, idx) => (
          <li key={idx}>
            <strong>{item.text}</strong> - Prediction: {item.prediction}
          </li>
        ))}
      </ul>
        
      
    </div>
  );
}

export default App;
