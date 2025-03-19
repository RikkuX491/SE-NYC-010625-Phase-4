function LoginForm(){
    return (
        <div className="new-hotel-form">
            <h2>Login</h2>
            <form>
                <input type="text" name="username" placeholder="Username" required />
                <button type="submit">Login</button>
            </form>
        </div>
    )
}

export default LoginForm;