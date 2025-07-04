import React, { useEffect, useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function History() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/tracking`)
      .then(res => res.json())
      .then(setItems);
  }, []);

  return (
    <div>
      <h2>History</h2>
      <ul>
        {items.map(i => (
          <li key={i.id}>{i.habit_id} - {i.date}</li>
        ))}
      </ul>
    </div>
  );
}
