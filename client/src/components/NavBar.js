import { NavLink } from "react-router-dom";

function NavBar({user, logOutUser}){
    return (
        <nav className="navbar">
            {user !== null ? 
                <>
                    <NavLink to="/">Home</NavLink>
                    <NavLink to="/add_hotel">Add Hotel</NavLink>
                    <NavLink to="/reviews">View All Reviews</NavLink>
                    <NavLink to="/my_reviews">My Reviews</NavLink>
                    <NavLink to="/add_review">Add Review</NavLink>
                    <NavLink onClick={logOutUser} to="/login">Log Out</NavLink>
                </>
                :
                <NavLink to="/login">Login</NavLink>
            }
        </nav>
    )
}

export default NavBar;