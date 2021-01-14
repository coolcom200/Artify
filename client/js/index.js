const URL = "http://localhost:5000"
const PRODUCTS_URL = URL + "/search?price_max=100"

const createProductCard = ({ _source: { product_name, description, price } }) => {
    const div = document.createElement("div");
    div.innerHTML = `<div class="col">
    <div class="card shadow-sm">
        <svg class="bd-placeholder-img card-img-top" width="100%" height="225"
            xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder: Thumbnail"
            preserveAspectRatio="xMidYMid slice" focusable="false">
        </svg>

        <div class="card-body">
            <h5 class="card-title text-truncate"> ${product_name} - $${price} </h5>
            <p class="card-text text-truncate">${description}</p>
        </div>
    </div>
    </div>`
    return div
}

const getProducts = async () => {
    response = await fetch(PRODUCTS_URL)
    if (response.ok) {
        response_json = await response.json()
        const { hits: { hits } } = response_json
        const products_location = document.querySelector("#products")
        for (let p of hits) {
            products_location.appendChild(
                createProductCard(p)
            )
        }

        console.log(hits)
        console.log(response_json)
    }
}



document.addEventListener("DOMContentLoaded", getProducts)