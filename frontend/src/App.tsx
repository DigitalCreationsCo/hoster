import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/index';
import Upload from './pages/upload';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" Component={Home} />
        <Route path="/upload" Component={Upload} />
      </Routes>
    </Router>
  )
}

export default App
