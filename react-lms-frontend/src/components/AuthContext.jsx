//import React, { useState } from "react";
import React, { createContext, useState } from "react";
import axios from "axios";
export const AuthContext = createContext();
const baseUrl = import.meta.env.VITE_API_URL; // ----- http://localhost:8000 // http://127.0.0.1:8000
/*
we can read import.meta.env.VITE_API_URL in any module in your Vite-powered React app. 
Vite injects all VITE_* vars onto the global import.meta.env object, 
so from any .js/.jsx/.ts/.tsx file we can import
*/

// Define the AuthProvider component, which will wrap children components and provide authentication context
export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [page, setPage] = useState(token ? "profile" : "login");  // Boolean("") === false // (falsy: "", null, undefined, 0, false, etc.)

  // Function to handle user login
  const login = async (username, password) => {    
    const res = await axios.post(`http://localhost:8000/api/token/`, { username, password }); // Send POST request to obtain JWT token
    const data = res.data;
    // Save the access token in state and localStorage
    setToken(data.access); // Use 'access' instead of 'token'
    localStorage.setItem("token", data.access); // Use 'access' instead of 'token'
    // Navigate to the profile page after login
    setPage("profile");
  };

  // Function to handle user logout
  const logout = () => {
    setToken(""); // Clear the token from state
    localStorage.removeItem("token"); // Remove the token from localStorage
    setPage("login"); // Navigate to the login page
  };

  // Function to handle user registration
  const register = async (username, email, password, role) => {
    // Send POST request to register a new user	
    //await axios.post("http://localhost:8000/api/user/auth/", { username, email, password, role });
    await axios.post(`${baseUrl}/api/user/auth/`, { username, email, password, role });
    // After registration, navigate to the login page
    setPage("login");
  };

  // Helper function to navigate to a specific page
  const goTo = (pageName) => setPage(pageName);

  // Provide the authentication context to child components
  return (
    <AuthContext.Provider value={{ token, login, logout, register, page, goTo }}>
      {children}
    </AuthContext.Provider>
  );
}


// import like: import { AuthContext, AuthProvider } from "./components/AuthContext";