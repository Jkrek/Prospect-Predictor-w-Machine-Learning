import React, { useState, useEffect } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './services.css';

function Services() {
  const [playerName, setPlayerName] = useState('');
  const [rowData, setRowData] = useState([]);
  const [columnDefs] = useState([
    { headerName: 'Service', field: 'service', sortable: true, filter: true },
    { headerName: 'Description', field: 'description', sortable: true, filter: true },
    { headerName: 'Price', field: 'price', sortable: true, filter: true },
  ]);

  const handleInputChange = (event) => {
    setPlayerName(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("Analyze button clicked");
    console.log("Player Name:", playerName);
    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: playerName }),
      });
      console.log("Response status:", response.status);
      const data = await response.json();
      console.log("Response data:", data);
      if (response.ok) {
        setRowData((prevRowData) => [
          ...prevRowData,
          {
            service: playerName,
            description: data.success,
            price: data.predicted_position,
          },
        ]);
      } else {
        console.error('Error:', data.error);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  useEffect(() => {
    // Initial static data
    const data = [
      { service: 'Quinn Ewers', description: 'Failure', price: '.63' },
      { service: 'Caleb Downs', description: 'Success', price: '.82' },
      { service: 'Harold Perkins', description: 'Success', price: '.79' },
    ];
    setRowData(data);
  }, []);

  return (
    <div className="services">
      <h1>PREDICT</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="playerName">Player Name:</label>
        <input
          type="text"
          id="playerName"
          value={playerName}
          onChange={handleInputChange}
          placeholder="Enter player name"
          required
        />
        <button type="submit">Analyze</button>
      </form>
      <div className="ag-theme-alpine" style={{ height: 400, width: '100%', marginTop: '20px' }}>
        <AgGridReact
          rowData={rowData}
          columnDefs={columnDefs}
          defaultColDef={{ flex: 1, minWidth: 100, filter: true, resizable: true }}
        />
      </div>
    </div>
  );
}

export default Services;
