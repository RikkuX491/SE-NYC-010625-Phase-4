import { NavLink } from "react-router-dom";

function NavBar({customer, logout}){

    return (
        <nav className="navbar">
            { customer ?
                <>
                    <NavLink to="/">Home</NavLink>
                    <NavLink to="/add_hotel">Add Hotel</NavLink>
                    <NavLink to="/login" onClick={logout}>Logout</NavLink>
                </> :
                <NavLink to="/login">Login</NavLink> 
            }
        </nav>
    )
}

export default NavBar;