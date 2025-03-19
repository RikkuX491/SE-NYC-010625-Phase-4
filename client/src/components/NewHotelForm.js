import { useState } from "react";
import { useOutletContext} from "react-router-dom";

function NewHotelForm() {

  const {addHotel} = useOutletContext()


  const [formData, setFormData] = useState({
    name: "",
    image: ""
  })

  function updateFormData(event){
    setFormData({...formData, [event.target.name]: event.target.value})
  }

  function handleSubmit(event){
    event.preventDefault()

    addHotel(formData)
    
    setFormData({
      name: "",
      image: ""
    })
  }

  return (
    <div className="new-hotel-form">
      <h2>New Hotel</h2>
      <form onSubmit={handleSubmit}>
        <input onChange={updateFormData} type="text" name="name" placeholder="Hotel name" value={formData.name} required />
        <input onChange={updateFormData} type="text" name="image" placeholder="Image URL" value={formData.image} required />
        <button type="submit">Add Hotel</button>
      </form>
    </div>
  );
}
  
  export default NewHotelForm;