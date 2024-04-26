const cupcakeList = $("#cupcake-list")

async function fillCupcakeList() {
    try {
    
        cupcakeList.empty()
        
        const response = await axios.get('http://127.0.0.1:5000/api/cupcakes')
        const cupcakes = response.data
        
        cupcakes.forEach(cupcake => {
            const $li = $("<li>").text(cupcake.flavor);
            
            cupcakeList.append($li);
        });
    } catch (error) {
        console.error("Error fetching cupcake", error)
    }
}

fillCupcakeList()

$('form').on('submit', async (e) => {
    e.preventDefault();
    
    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = $('#rating').val();
    let image = $('#image').val();
    
    await axios.post('/api/cupcakes', {
        flavor: flavor,
        size: size,
        rating: rating,
        image: image
    })
    
    fillCupcakeList();
    
    [$('#flavor'), $('#size'), $('#rating'), $('#image')].forEach(field => {
        field.val('');
    })
})