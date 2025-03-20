import UserReview from "./UserReview";
import { useOutletContext } from "react-router-dom";

function UserReviewList(){

    const {user} = useOutletContext()

    let userReviewComponents = null

    if(user){
        userReviewComponents = user.reviews.map(review => {
            return <UserReview key={review.id} review={review}/>
        })
        return <>{user.reviews.length > 0 ? <ul>{userReviewComponents}</ul> : <h1>You have no reviews!</h1>}</>
    }

    else{
        return null;
    }
}

export default UserReviewList;