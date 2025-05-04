import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Homepage from "./components/Homepage";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
      <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/homepage" element={<ProtectedRoute />}>
          <Route index element={<Navigate to="/homepage/chat" replace />} />
          <Route path="chat" element={<Homepage />} />
          <Route path="chat/:chatId" element={<Homepage />} />
        </Route>
        </Routes>
    </Router>  
  );
}

export default App;
