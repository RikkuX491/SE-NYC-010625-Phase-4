import {useState} from 'react';

import { useOutletContext } from 'react-router-dom';

function LoginForm(){

    const [formData, setFormData] = useState({
        username: "",
        password: ""
    })

    const {logInUser} = useOutletContext()

    function updateFormData(event){
        setFormData({...formData, [event.target.name]: event.target.value})
    }

    function handleSubmit(event){
        event.preventDefault()

        logInUser(formData)
    }

    return (
        <div className="new-hotel-form">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
            <input onChange={updateFormData} type="text" name="username" placeholder="Username" value={formData.username} required />
            <input onChange={updateFormData} type="password" name="password" placeholder="Password" value={formData.password} required />
            <button type="submit">Login</button>
        </form>
    </div>
    )
}

export default LoginForm;