import Header from "./Header";
import { useState, useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import NavBar from "./NavBar";

function App(){

    const navigate = useNavigate()

    const [hotels, setHotels] = useState([])

    useEffect(() => {
        // GET request - Retrieve all hotels and update the 'hotels' state with the hotel data.
        fetch('/hotels')
        .then(response => response.json())
        .then(hotelsData => setHotels(hotelsData))
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

    return (
      <div className="app">
        <NavBar/>
        <Header/>
        <Outlet context={{hotels: hotels, addHotel: addHotel, deleteHotel: deleteHotel, updateHotel: updateHotel}}/>
      </div>
    );
}

export default App;