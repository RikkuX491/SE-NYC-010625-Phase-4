import { useState } from "react";
import { useOutletContext } from "react-router-dom";

function LoginForm(){

    const { login } = useOutletContext()

    const [username, setUsername] = useState("")

    function handleSubmit(event){
        event.preventDefault()
        
        const formData = {
            username: username
        }
        
        fetch('/login', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if(response.ok){
                response.json().then(customerData => {
                    // call our login() function and pass in the customer data that will be used to update the customer state
                    login(customerData)
                })
            }
            else{
                response.json().then(errorObject => {
                    // display error message
                    alert(`Error: ${errorObject.error}`)
                })
            }
        })
    }

    function updateUsername(event){
        setUsername(event.target.value)
    }

    return (
        <div className="new-hotel-form">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input onChange={updateUsername} type="text" name="username" placeholder="Username" value={username} required />
                <button type="submit">Login</button>
            </form>
        </div>
    )
}

export default LoginForm;