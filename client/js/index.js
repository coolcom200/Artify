const PRODUCTS_URL = 'api/search';

const createProductCard = ({
    product_name, description, price, images
}) => {
    const div = document.createElement('div');
    const image = images.length > 0 ? images[0] : {}
    div.innerHTML = `<div class="col">
    <div class="card shadow-sm">
        <img class="card-img-top" width="100%" height="225" src="api/image/${image.file_path}/">
        </img>

        <div class="card-body">
            <h5 class="card-title text-truncate"> ${product_name} - $${price} </h5>
            <p class="card-text text-truncate">${description}</p>
        </div>
    </div>
    </div>`;
    return div;
};

const getProducts = async (_, queryParams) => {
    let url = PRODUCTS_URL
    if (queryParams) {
        url += `?${queryParams}`
    }
    response = await fetch(url);
    if (response.ok) {
        response_json = await response.json();
        const products = response_json;
        const products_location = document.querySelector('#products');
        removeChildren(products_location)
        for (let p of products) {
            products_location.appendChild(createProductCard(p));
        }
    }
};

const search = async () => {
    const searchQuery = document.getElementById("searchQuery").value;
    const minPrice = document.getElementById("searchPriceMin").value;
    const maxPrice = document.getElementById("searchPriceMax").value;
    let urlQuery = []
   
    if (searchQuery && searchQuery.trim() !== "") {
        urlQuery.push(`query=${searchQuery}`)
    }
    
    if (minPrice && minPrice.trim() !== "") {
        urlQuery.push(`price_min=${minPrice}`)
    }
    
    if (maxPrice && maxPrice.trim() !== "") {
        urlQuery.push(`price_max=${maxPrice}`)
    }
    getProducts(undefined, urlQuery.join("&"))
}

const removeChildren = (node) => {
    while (node.lastElementChild) {
        node.removeChild(node.lastElementChild);
  }
}

document.addEventListener('DOMContentLoaded', getProducts);
