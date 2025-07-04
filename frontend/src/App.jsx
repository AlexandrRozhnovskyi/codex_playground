import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HabitList from './pages/HabitList';
import AddHabit from './pages/AddHabit';
import History from './pages/History';

export default function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Habits</Link> |{' '}
        <Link to="/add">Add Habit</Link> |{' '}
        <Link to="/history">History</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HabitList />} />
        <Route path="/add" element={<AddHabit />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </Router>
  );
}
