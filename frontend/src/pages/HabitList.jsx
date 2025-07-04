import React, { useEffect, useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function HabitList() {
  const [habits, setHabits] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/habits`)
      .then(res => res.json())
      .then(setHabits);
  }, []);

  return (
    <div>
      <h2>Habits</h2>
      <ul>
        {habits.map(h => (
          <li key={h.id}>{h.title} - {h.frequency}</li>
        ))}
      </ul>
    </div>
  );
}
