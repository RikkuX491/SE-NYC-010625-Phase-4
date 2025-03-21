import { Link, useOutletContext } from "react-router-dom";

function Hotel({hotel}){

    const { user } = useOutletContext()
    console.log(user)

    return (
        <li className="hotel">
            <img src={hotel.image} alt={hotel.name}/>
            <h4>{hotel.name}</h4>
            {(user && user.type === "admin") ? <Link to={`/hotels/${hotel.id}`}>View Hotel Profile</Link> : null}
        </li>
    );
}

export default Hotel;