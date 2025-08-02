
import { useContext } from "react";
import { AuthContext } from "../components/AuthContext.jsx";

// Custom hook to access the AuthContext easily in components
export function useAuth() {
  // Return the current context value for AuthContext
  return useContext(AuthContext);
}
