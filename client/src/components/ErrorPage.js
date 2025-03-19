import NavBar from './NavBar';

function ErrorPage(){
    return (
        <div className="app">
            <NavBar/>
            <h1>Whoops! That page doesn't exist!</h1>
        </div>
    )
}

export default ErrorPage;