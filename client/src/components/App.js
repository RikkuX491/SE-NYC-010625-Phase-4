import Header from "./Header";
import { useState, useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import NavBar from "./NavBar";

function App(){

    const [hotels, setHotels] = useState([])

    const navigate = useNavigate();

    // const baseURL = "http://localhost:7777"

    useEffect(getHotels, [])

    function getHotels(){
        // GET request - Write the code to make a GET request to '/hotels' to retrieve all hotels and update the 'hotels' state with the hotel data.
        fetch("/hotels")
        .then(response => response.json())
        .then(hotelsData => setHotels(hotelsData))
    }

    function addHotel(newHotel){
        // POST request - Write the code to make a POST request to '/hotels' to create a new hotel and update the 'hotels' state to add the new hotel to the state.
        // newHotel - contains an object with the new hotel data that should be used for the POST request.
        fetch("/hotels", {
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
            else{
                response.json().then(errorObject => {
                    alert(`Error: ${errorObject.error}`)
                })
            }
        })
    }

    function updateHotel(id, hotelDataForUpdate){
        // PATCH request - Write the code to make a PATCH request to `/hotels/${id}` (use string interpolation since the value of the id parameter should be incorporated into the string). You should update a hotel by id and update the 'hotels' state with the updated hotel data.
        // id - contains a number that refers to the id for the hotel that should be updated.
        // hotelDataForUpdate - contains an object with the hotel data for the PATCH request.
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
                // update the hotel data
                response.json().then(updatedHotelData => {
                    const updatedHotelsArray = hotels.map(hotel => {
                        if(hotel.id === updatedHotelData.id){
                            return updatedHotelData
                        }
                        else{
                            return hotel
                        }
                    })
                    setHotels(updatedHotelsArray)
                })
            }
            else{
                response.json().then(errorObject => {
                    alert(`Error: ${errorObject.error}`)
                })
            }
        })
    }

    function deleteHotel(id){
        // DELETE request - Write the code to make a DELETE request to `/hotels/${id}` (use string interpolation since the value of the id parameter should be incorporated into the string). You should delete a hotel by id and update the 'hotels' state to remove the hotel from the state.
        // id - contains a number that refers to the id for the hotel that should be deleted.
        fetch(`/hotels/${id}`, {
            method: "DELETE"
        })
        .then(response => {
            if(response.ok){
                const updatedHotelsArray = hotels.filter(hotel => {
                    return hotel.id !== id
                })
                setHotels(updatedHotelsArray)
            }
            else{
                response.json().then(errorObject => {
                    alert(`Error: ${errorObject.error}`)
                })
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