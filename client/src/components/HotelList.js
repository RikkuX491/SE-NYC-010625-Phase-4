import Hotel from './Hotel';
import { useOutletContext } from "react-router-dom";

function HotelList(){

    const {hotels} = useOutletContext()

    const hotelComponents = hotels.map(hotel => {
        return <Hotel key={hotel.id} hotel={hotel}/>
    })

    return (
        <ul className="hotel-list">{hotelComponents}</ul>
    );
}

export default HotelList;