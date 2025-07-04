import React, { useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function AddHabit() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [frequency, setFrequency] = useState('daily');
  const [userId, setUserId] = useState(1);

  const handleSubmit = e => {
    e.preventDefault();
    fetch(`${API_URL}/habits`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description, frequency, user_id: Number(userId) })
    }).then(() => {
      setTitle('');
      setDescription('');
    });
  };

  return (
    <div>
      <h2>Add Habit</h2>
      <form onSubmit={handleSubmit}>
        <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title" />
        <input value={description} onChange={e => setDescription(e.target.value)} placeholder="Description" />
        <select value={frequency} onChange={e => setFrequency(e.target.value)}>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
        <input value={userId} onChange={e => setUserId(e.target.value)} type="number" placeholder="User ID" />
        <button type="submit">Add</button>
      </form>
    </div>
  );
}
