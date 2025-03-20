import Review from "./Review";
import { useOutletContext } from "react-router-dom";

function ReviewList(){

    const {reviews} = useOutletContext()

    const reviewComponents = reviews.map(review => {
        return <Review key={review.id} review={review}/>
    })

    return (
        <ul>{reviewComponents}</ul>
    );
}

export default ReviewList;