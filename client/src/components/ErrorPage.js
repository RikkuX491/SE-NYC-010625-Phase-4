import NavBar from './NavBar';
import Header from './Header';

function ErrorPage(){
    return (
        <div className="app">
            <NavBar/>
            <Header/>
            <h1>Whoops! That page doesn't exist!</h1>
        </div>
    )
}

export default ErrorPage;