import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import {createBrowserRouter, RouterProvider} from "react-router-dom";

import App from './components/App';
import ErrorPage from './components/ErrorPage';
import HotelList from './components/HotelList';
import NewHotelForm from './components/NewHotelForm';
import HotelProfile from './components/HotelProfile';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
    errorElement: <ErrorPage/>,
    children: [
      {
        path: "/",
        element: <HotelList/>
      },
      {
        path: '/add_hotel',
        element: <NewHotelForm/>
      },
      {
        path: "/hotels/:id",
        element: <HotelProfile/>
      }
    ]
  }
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<RouterProvider router={router} />);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
