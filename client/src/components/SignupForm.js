import { useState } from "react";

import { useOutletContext } from "react-router-dom";

function SignupForm(){
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        username: "",
        password: ""
    })

    const { signup } = useOutletContext()

    function updateFormData(event){
        setFormData({...formData, [event.target.name]: event.target.value})
    }

    function handleSubmit(event){
        event.preventDefault()

        signup(formData)
    }

    return (
        <div className="new-hotel-form">
            <h2>Signup</h2>
            <form onSubmit={handleSubmit}>
                <input onChange={updateFormData} type="text" name="first_name" placeholder="First Name" value={formData.first_name} required />
                <input onChange={updateFormData} type="text" name="last_name" placeholder="Last Name" value={formData.last_name} required />
                <input onChange={updateFormData} type="text" name="username" placeholder="Username" value={formData.username} required />
                <input onChange={updateFormData} type="password" name="password" placeholder="Password" value={formData.password} required />
                <button type="submit">Signup</button>
            </form>
        </div>
    );
}

export default SignupForm;