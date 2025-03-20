import { Link } from "react-router-dom";

function Hotel({hotel}){

    return (
        <li className="hotel">
            <img src={hotel.image} alt={hotel.name}/>
            <h4>{hotel.name}</h4>
            <Link to={`/hotels/${hotel.id}`}>View Hotel Profile</Link>
        </li>
    );
}

export default Hotel;