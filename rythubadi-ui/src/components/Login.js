import { useNavigate } from "react-router-dom";
import logo from '../rythubadi.png';
import '../App.css';

function Login() {
  const navigate = useNavigate();
  
  return (
    <div className="App">
        <img src={logo} className="App-logo" alt="logo" />
        <div class="login-container">
          <h2>Login</h2>
          <form>
            <label>Email</label>
            <input type="text" placeholder="Enter your email" />

            <label>Password</label>
            <input type="password" placeholder="Enter your password" />

            <button type="submit">Login</button>

            <p class="signup-text">Not registered? <span onClick={() => navigate("/signup")}>Signup</span></p>
          </form>
        </div>
    </div>
  );
}

export default Login;