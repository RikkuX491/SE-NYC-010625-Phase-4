css_code = """
    <style>
        * {
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            box-sizing: border-box;
        }
        
        body {
            padding: 1rem;
            text-align: center;
            background-color: #fafafa;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        header {
            padding: 0.5rem;
            width: 100%;
            color: white;
            background-color: black;
        }

        #restaurant-menu {
            display: flex;
            overflow-x: auto;
            margin: 1rem 0;
            max-width: calc(100vw - 2rem);
        }

        #restaurant-menu img {
            flex: 0 1 auto;
            height: 150px;
            margin-right: 0.5rem;
            cursor: pointer;
        }

        #restaurant-menu img:last-child {
            margin-right: 0;
        }

        #food-detail {
            position: relative;
        }

        .detail-image {
            height: 350px;
        }

        .name {
            position: absolute;
            left: 10px;
            padding: 0.25rem 5rem 0.25rem 1rem;
            background-color: rgba(255, 255, 255, 0.8);
            bottom: 60px;
        }
    </style>
"""

js_code = """
    <script>
        document.addEventListener('DOMContentLoaded', updateDOM)

        function updateDOM(){
            fetch("http://localhost:7777/burgers")
            .then(response => response.json())
            .then(burgers => {
                burgers.forEach(addBurgerToRestaurantMenu)
                displayBurgerDetails(burgers[0])
            })
        }

        function addBurgerToRestaurantMenu(burger){
            const imgElement = document.createElement('img')
            imgElement.src = burger.image
            imgElement.addEventListener('click', () => displayBurgerDetails(burger))
            const restaurantMenu = document.getElementById('restaurant-menu')
            restaurantMenu.appendChild(imgElement)
        }

        function displayBurgerDetails(burger){
            const detailImageElement = document.querySelector('.detail-image')
            detailImageElement.src = burger.image
            const nameElement = document.querySelector('.name')
            nameElement.textContent = burger.name
            const descriptionDisplayElement = document.getElementById('description-display')
            descriptionDisplayElement.textContent = burger.description
        }
    </script>
"""

flatburger_html_code = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8" />
            <title>Flatburger</title>
            {css_code}
            {js_code}
        </head>

        <body>
            <header>
                <h3>🍔 Flatburger 🍔</h3>
            </header>

            <!-- Restaurant Menu -->
            <div id="restaurant-menu">
                <!-- Food Images Here -->
            </div>

            <!-- Food Details -->
            <div id="food-detail">
                <img class="detail-image" src="https://raw.githubusercontent.com/RikkuX491/SE-NYC-082624-Phase-1/refs/heads/03_solution/assets/image-placeholder.jpg" alt="Insert Name Here" />
                <h2 class="name">Insert Name Here</h2>
            </div>

            <h3>Description:</h3>
            <p id='description-display'>
                Insert food description here
            </p>
        </body>
    </html>
"""