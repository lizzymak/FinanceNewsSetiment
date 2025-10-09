import './App.css';
import { useState } from 'react';

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const predict = () => {
    //const response = axios
  }

  return (
    <div className="App">
      <h1>News setiment analyzer</h1>
      <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Enter company or topic..." />
      <button onClick={predict}>Analyze</button>
      <p>{results}</p>
    </div>
  );
}

export default App;
