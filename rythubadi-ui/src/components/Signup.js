import { useNavigate } from "react-router-dom";
import logo from '../rythubadi.png';
import '../App.css';

function Signup() {
    const navigate = useNavigate();

    return (
    <div className="App">
        <img src={logo} className="App-logo" alt="logo" />
        <div class="signup-container">
          <h2>Signup</h2>
          <form>
            <label>Email</label>
            <input type="text" placeholder="Enter your email" />

            <label>Password</label>
            <input type="password" placeholder="Enter your password" />

            <label>Confirm Password</label>
            <input type="password" placeholder="Renter your password" />

            <button type="submit">Signup</button>

            <p class="signup-text">Already registered? <span onClick={() => navigate("/")}>Login</span></p>
          </form>
        </div>
    </div>    
    )
}

export default Signup;