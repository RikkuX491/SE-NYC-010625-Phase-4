import { useState, useEffect } from "react";
import {useParams, useOutletContext, useNavigate} from "react-router-dom";

function HotelProfile(){

    const [hotel, setHotel] = useState(null)
    const [displayForm, setDisplayForm] = useState(false)
    const [formData, setFormData] = useState({
        name: "",
        image: ""
    })

    // id - contains a number that refers to the id for the hotel that should be retrieved via fetch() (GET request) in the callback function in useEffect().
    const {id} = useParams()

    const {deleteHotel, updateHotel} = useOutletContext()
    const navigate = useNavigate()

    useEffect(getHotel, [])

    function getHotel(){
        // GET request - Write the code to make a GET request to `/hotels/${id}` (use string interpolation since the value of the id variable should be incorporated into the string). You should retrieve a hotel by id and update the 'hotel' state with the hotel data.
    }

    function handleDeleteButtonClick(){
        deleteHotel(hotel.id)
        setHotel(null)
        navigate('/')
    }

    function toggleDisplayForm(){
        setDisplayForm(displayForm => !displayForm)
    }

    function handleSubmit(event){
        event.preventDefault()

        updateHotel(hotel.id, formData)
        setHotel({...hotel, ...formData})

        toggleDisplayForm()
    }

    function updateFormData(event){
        setFormData({...formData, [event.target.name]: event.target.value})
    }

    return (
        <>
            {hotel ?
            <div className="hotel-profile">
                <img src={hotel.image} alt={hotel.name}/>
                <h4>{hotel.name}</h4>
                { !displayForm ?
                <div className="button-div">
                    <button onClick={toggleDisplayForm} className="update-button">Update Hotel</button>
                    <button onClick={handleDeleteButtonClick} className="delete-button">Delete Hotel</button>
                </div> :
                <form onSubmit={handleSubmit} className="edit-hotel">
                    <input onChange={updateFormData} type="text" name="name" placeholder="Hotel name" value={formData.name} />
                    <input onChange={updateFormData} type="text" name="image" placeholder="Image URL" value={formData.image} />
                    <button type="submit">Save Changes</button>
                </form>
                }
            </div> :
            null
            }
        </>
    );
}

export default HotelProfile;