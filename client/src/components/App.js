import Header from "./Header";
import { useState, useEffect } from "react";
import { Outlet, useNavigate, Navigate } from "react-router-dom";
import NavBar from "./NavBar";

function App(){

    const navigate = useNavigate()

    const [hotels, setHotels] = useState([])
    const [customer, setCustomer] = useState(null)

    useEffect(() => {
        // GET request - Retrieve all hotels and update the 'hotels' state with the hotel data.
        fetch('/hotels')
        .then(response => response.json())
        .then(hotelsData => setHotels(hotelsData))
    }, [])

    // Check if the user is logged in by checking if the customer state is currently null
    useEffect(() => {
        fetch('/check_session')
        .then(response => {
            if(response.ok){
                response.json().then(customerData => {
                    // update the customer state with the customer data for the customer that should be logged in
                    setCustomer(customerData)
                })
            }
            else{
                // Navigate the user to the login page to log in to their account
                navigate('/login')
            }
        })
    }, [])

    function addHotel(newHotel){
        // POST request - Create a new hotel and update the 'hotels' state to add the new hotel to the state.
        fetch('/hotels', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(newHotel)
        })
        .then(response => {
            if(response.ok){
                response.json().then(newHotelData => {
                    setHotels([...hotels, newHotelData])
                    navigate('/')
                })
            }
            else if(response.status === 400){
                response.json().then(errorData => alert(`Error: ${errorData.error}`))
            }
            else{
                response.json().then(() => alert("Error: Something went wrong."))
            }
        })
    }

    function updateHotel(id, hotelDataForUpdate, setHotelFromHotelProfile){
        // PATCH request - Update a hotel by id and update the 'hotels' state with the updated hotel data.
        fetch(`/hotels/${id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(hotelDataForUpdate)
        })
        .then(response => {
            if(response.ok){
                response.json().then(updatedHotelData => {
                    setHotelFromHotelProfile(updatedHotelData)
                    setHotels(hotels => hotels.map(hotel => {
                        if(hotel.id === updatedHotelData.id){
                            return updatedHotelData
                        }
                        else{
                            return hotel
                        }
                    }))
                })
            }
            else if(response.status === 400 || response.status === 404){
                response.json().then(errorData => {
                    alert(`Error: ${errorData.error}`)
                })
            }
            else{
                response.json().then(() => {
                    alert("Error: Something went wrong.")
                })
            }
        })
    }

    function deleteHotel(id){
        // DELETE request - Delete a hotel by id and update the 'hotels' state to remove the hotel from the state.
        fetch(`/hotels/${id}`, {
            method: "DELETE"
        })
        .then(response => {
            if(response.ok){
                setHotels(hotels => hotels.filter(hotel => {
                    return hotel.id !== id
                }))
            }
            else if(response.status === 404){
                response.json().then(errorData => alert(`Error: ${errorData.error}`))
            }
        })
    }

    function login(customerData){
        setCustomer(customerData)
        navigate('/')
    }

    function logout(){
        fetch('/logout', {
            method: "DELETE"
        })
        .then(response => {
            if(response.ok){
                setCustomer(null)
            }
            else{
                alert("Error: Unable to log out user!")
            }
        })
    }

    return (
      <div className="app">
        <NavBar customer={customer} logout={logout}/>
        <Header/>
        {customer ? <h1>Hello {customer.username}!</h1> : null}
        <Outlet context={
            {
                hotels: hotels,
                addHotel: addHotel,
                deleteHotel: deleteHotel,
                updateHotel: updateHotel,
                login: login
            }
        }/>
      </div>
    );
}

export default App;