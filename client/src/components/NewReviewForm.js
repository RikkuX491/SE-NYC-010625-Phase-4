import { useState, useEffect } from "react";
import { useOutletContext} from "react-router-dom";

function NewReviewForm(){
    const {addReview, hotels, user} = useOutletContext()

    const [formData, setFormData] = useState({
        rating: "1",
        text: "",
        hotel_id: ""
    })

    const optionElements = hotels.map(hotel => {
        return <option key={hotel.id} value={hotel.id}>{hotel.id}: {hotel.name}</option>
    })

    useEffect(() => {
        if(hotels.length > 0){
            setFormData(formData => {
                return {...formData, hotel_id: hotels[0].id}
            })
        }
    }, [hotels])

    function updateFormData(event){
        setFormData({...formData, [event.target.name]: event.target.value})
    }

    function handleSubmit(event){
        event.preventDefault()
   
        const newReview = {
            ...formData,
            rating: Number(formData.rating),
            hotel_id: Number(formData.hotel_id),
            user_id: user.id
        }
        
        addReview(newReview)
    }

    return (
        <div>
          <h2>New Review</h2>
          <form onSubmit={handleSubmit}>
            <label htmlFor="rating-select">Rating: </label>
            <select onChange={updateFormData} id="rating-select" name="rating" value={formData.rating}>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
            </select>
            <br/>
            <br/>
            <label htmlFor="hotel-select">Hotel: </label>
            <select onChange={updateFormData} id="hotel-select" name="hotel_id" value={formData.hotel_id}>
                {optionElements}
            </select>
            <br/>
            <br/>
            <label htmlFor="text-textarea">Text: </label>
            <textarea onChange={updateFormData} id="text-textarea" type="text" name="text" placeholder="Write your review here..." value={formData.text} required></textarea>
            <button type="submit">Submit Review</button>
          </form>
        </div>
    );
}

export default NewReviewForm;