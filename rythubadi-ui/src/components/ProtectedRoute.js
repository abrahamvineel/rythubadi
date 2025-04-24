import React from 'react';
import {Navigate, Outlet} from 'react-router-dom';

function ProtectedRoute() {
    const isAuthenticated = localStorage.getItem('authToken');
    console.log('is ', isAuthenticated)
      return isAuthenticated ? <Outlet /> : <Navigate to="/" />;
}

export default ProtectedRoute;