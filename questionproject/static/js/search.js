const inputElem = document.getElementById("searchInput")

function handleSearchItems(query) {
    const url = `/questions/search?q=${query}`;
    console.log(url)
    fetch(url, {
        method: 'GET', 
        headers: {
        'Accept': 'application/json'
    }
    })
    .then(response => response.json())
    .then(data => {
        console.log("data is", data)
        searchItems = data.questions
        console.log(searchItems)
        const searchContainer = document.querySelector(".search-results");
        searchContainer.replaceChildren();
        searchItems.forEach(item => {
            const searchItemTemplate = document.querySelector(".search-result-item.template");
            
            const newSearchItem = searchItemTemplate.cloneNode(true);
            
            newSearchItem.style.display = 'block';
            newSearchItem.querySelector(".search-item-title").textContent = item.title;
            newSearchItem.querySelector(".search-item-content").textContent = item.content;
            newSearchItem.querySelector(".search-item-link").href = `/questions/${item.id}/detail/`;
            searchContainer.appendChild(newSearchItem);
            console.log(item.title);
        });
        
        
        console.log('New answer added:');
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
    console.log(query); 
}

const handleSearch = debounce((query) => handleSearchItems(query), 300)

inputElem.addEventListener('input', (e) => { handleSearch(e.target.value); });
