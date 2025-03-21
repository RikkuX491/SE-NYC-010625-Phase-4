import { NavLink } from "react-router-dom";

function NavBar({user, logOutUser}){

    function getUserNavLinks(){
        if(user.type === "customer"){
            return <>
                <NavLink to="/">Home</NavLink>
                <NavLink to="/reviews">View All Reviews</NavLink>
                <NavLink to="/my_reviews">My Reviews</NavLink>
                <NavLink to="/add_review">Add Review</NavLink>
                <NavLink onClick={logOutUser} to="/login">Log Out</NavLink>
            </>
        }
        else if(user.type === "admin"){
            return <>
                <NavLink to="/">Home</NavLink>
                <NavLink to="/add_hotel">Add Hotel</NavLink>
                <NavLink to="/reviews">View All Reviews</NavLink>
                <NavLink onClick={logOutUser} to="/login">Log Out</NavLink>
            </>
        }
        else{
            return null
        }
    }

    function getLoginAndSignupNavLink(){
        return (
            <>
                <NavLink to="/login">Login</NavLink>
                <NavLink to="/signup">Signup</NavLink>
            </>
        );
    }

    return (
        <nav className="navbar">
            {user !== null ? 
                getUserNavLinks()
                :
                getLoginAndSignupNavLink()
            }
        </nav>
    )
}

export default NavBar;