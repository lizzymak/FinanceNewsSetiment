import React from 'react';
import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  return (
    <div className="App">
      <h1>News setiment analyzer</h1>
      <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Enter company or topic..." />
      <button>Analyze</button>
    </div>
  );
}

export default App;
