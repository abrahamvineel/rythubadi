import {useState} from 'react'
import { useNavigate } from "react-router-dom";
import axios from "axios";
import logo from '../rythubadi.png';
import '../App.css';

function Signup() {

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });
  
  const navigate = useNavigate();

  const handleFormData = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  }

  const handleSubmit = async (event) => {
    console.log('event', event);

    console.log('email', formData.email);

    console.log('password', formData.password);
    event.preventDefault();

    if(formData.password !== formData.confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    
    try {
      const response = await axios.post('http://localhost:8080/api/users', {
        email: formData.email, 
        password: formData.password
      });

      if (response.ok) {
        navigate("/")
      } else {
        console.error('Signup error');
      }

    } catch(error) {
      console.error('Signup error', error);
    }
  }

    return (
    <div className="App">
        <img src={logo} className="App-logo" alt="logo" />
        <div class="signup-container">
          <h2>Signup</h2>
          <form onSubmit={handleSubmit}>
            <label>Email</label>
            <input id="email" name="email" type="text" value={formData.email} onChange={handleFormData} required/>

            <label>Password</label>
            <input id="password" name="password" type="password" value={formData.password} onChange={handleFormData} required/>

            <label>Confirm Password</label>
            <input id="confirmPassword" name="confirmPassword" type="password" value={formData.confirmPassword} onChange={handleFormData} required/>

            <button type="submit">Signup</button>

            <p class="signup-text">Already registered? <span onClick={() => navigate("/")}>Login</span></p>
          </form>
        </div>
    </div>    
    )
}

export default Signup;