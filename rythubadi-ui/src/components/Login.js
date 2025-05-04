import { useNavigate } from "react-router-dom";
import logo from '../rythubadi.png';
import axios from "axios";
import {useState} from 'react'
import '../App.css';

function Login() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
      email: '',
      password: ''
    });

    const handleFormData = (e) => {
      setFormData({...formData, [e.target.name]: e.target.value});
    }  

    const handleSubmit = async (event) => {
      event.preventDefault();

      try {
        const response = await axios.post('http://localhost:8080/api/users/login', {
          email: formData.email, 
          password: formData.password
        })
        if(response.status === 200) {
          const token = response.data.token;
          if(token) {
            const email = response.data.email;
            localStorage.setItem('authToken', token);
            localStorage.setItem('email', email);
            navigate('/homepage', { state: { email: email } });
          }
        } else if (response.status === 401) {
          alert('Invalid credentials');
        }
      } catch(error) {
        alert('Invalid credentials');
        navigate('/')
      }
    }
  
  return (
    <div className="App">
        <img src={logo} className="App-logo" alt="logo" />
        <div class="login-container">
          <h2>Login</h2>
          <form onSubmit={handleSubmit}>
            <label>Email</label>
            <input id="email" name="email" type="text" value={formData.email} onChange={handleFormData} required/>

            <label>Password</label>
            <input id="password" name="password" type="password" value={formData.password} onChange={handleFormData} required/>

            <button type="submit">Login</button>

            <p class="signup-text">Not registered? <span onClick={() => navigate("/signup")}>Signup</span></p>
          </form>
        </div>
    </div>
  );
}

export default Login;