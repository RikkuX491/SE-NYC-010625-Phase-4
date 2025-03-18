import { NavLink } from "react-router-dom";

function NavBar(){
    return (
        <nav className="navbar">
            <NavLink to="/">Home</NavLink>
            <NavLink to="/add_hotel">Add Hotel</NavLink>
        </nav>
    )
}

export default NavBar;