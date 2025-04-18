import logo from './rythubadi.png';
import './App.css';

function App() {
  return (
    <div className="App">
        <img src={logo} className="App-logo" alt="logo" />

      {/* <header className="App-header">
      </header> */}
        <div class="login-container">
          <h2>Login</h2>
          <form>
            <label>Email</label>
            <input type="text" placeholder="Enter your email" />

            <label>Password</label>
            <input type="password" placeholder="Enter your password" />

            <button type="submit">Login</button>

            <p class="signup-text">Not registered? <a href="/">Signup</a></p>
          </form>
        </div>
    </div>
  );
}

export default App;
