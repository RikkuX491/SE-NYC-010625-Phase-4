import { useState } from "react";

import { useOutletContext } from "react-router-dom";

function UserReview({review}){

    const [displayForm, setDisplayForm] = useState(false)

    const [formData, setFormData] = useState({
        rating: review.rating,
        text: review.text
    })

    const {updateReview, deleteReview} = useOutletContext()

    let stars = ""
    for(let index = 1; index <= review.rating; index++){
        stars += "⭐"
    }

    function toggleDisplayForm(){
        setDisplayForm(!displayForm)
    }

    function updateFormData(event){
        setFormData({...formData, [event.target.name]: event.target.value})
    }

    function handleSubmit(event){
        event.preventDefault()
        updateReview(review.id, {...formData, rating: Number(formData.rating)})
        toggleDisplayForm()
    }

    function handleDeleteButtonClick(){
        deleteReview(review.id)
    }

    return (
        <>
            <li>
                {!displayForm ?
                    <div>
                        <h1>Review # {review.id}</h1>
                        <h2>Rating: {stars}</h2>
                    </div>
                    :
                    null}
                <h2>Text: {review.text}</h2>
                <h2>This review was left for {review.hotel.name}</h2>
                {!displayForm ?
                    <div className="button-div">
                        <button onClick={toggleDisplayForm} className="update-button">Update Review</button>
                        <button onClick={handleDeleteButtonClick}>Delete Review</button>
                    </div> :
                    <form onSubmit={handleSubmit} className="edit-hotel">
                        <label htmlFor="rating-select">Rating: </label>
                        <select onChange={updateFormData} id="rating-select" name="rating" value={formData.rating}>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                        <label htmlFor="text-input">Text: </label>
                        <input onChange={updateFormData} type="text" id="text-input" name="text" placeholder="Text value" value={formData.text} />
                        <button className="update-button" type="submit">Save Changes</button>
                    </form>}
            </li>
            <br/>
        </>
    )
}

export default UserReview;