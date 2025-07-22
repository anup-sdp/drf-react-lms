import React from "react"; // Import the core React library for building UI components
import ReactDOM from "react-dom/client"; // Import ReactDOM for rendering React components to the DOM (using the modern root API)
import App from "./App.jsx"; // Import the main App component
import "./index.css" // Import global CSS styles for the application  // @import "tailwindcss";
import { AuthProvider } from "./components/AuthContext.jsx"; // Import the AuthProvider for authentication context

// Entry point: Render the App component into the root DOM node
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode> {/* Enable additional checks and warnings for development */}
    <AuthProvider> {/* Provide authentication context to the entire app */}
      <App /> {/* Render the main App component */}
    </AuthProvider>
  </React.StrictMode>
);


// React Hooks: (useState, useReducer, useContext, useEffect, useLayoutEffect, useInsertionEffect, useMemo, useCallback, useFetch, etc)
// https://www.geeksforgeeks.org/reactjs/reactjs-hooks/

/*
Context:
Context in React is used to share the data through the React Components without passing 
the props manually for every level of the component tree. It allows the data 
to be accessed globally throughout the application and enable efficient state management.
(instead of passing props)
*/
// vs redux: https://www.geeksforgeeks.org/web-tech/introduction-to-react-redux/



