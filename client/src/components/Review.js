function Review({review}){

    let stars = ""
    for(let index = 1; index <= review.rating; index++){
        stars += "⭐"
    }

    return (
        <>
            <li>
                <h1>Review # {review.id}</h1>
                <h2>Rating: {stars}</h2>
                <h2>Text: {review.text}</h2>
                <h2>This review was left by {review.user.username} for {review.hotel.name}</h2>
            </li>
            <br/>
        </>
    )
}

export default Review;