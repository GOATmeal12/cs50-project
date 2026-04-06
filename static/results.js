searchBox = document.getElementById("search")
resultsList = document.getElementById("results")

searchBox.addEventListener("input", async () => {
    const query = searchBox.value;

    if (query.length < 2){
        resultsList.innerHTML ="";
        return;
    }

   

    const response = await fetch(`/search-pieces?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    

    if (data.length === 0) {
    resultsList.innerHTML = `
        <div class="alert alert-info mb-0 text-center">
            No results found. Add it manually
            <form method="POST">
                <input name="title" class="form-control mb-2" value="${query}" required>
                <input name="composer" class="form-control mb-2" placeholder="Composer (optional)">
                <button type="submit" class="button">Add Piece</button>
            </form>
        </div>
    `;
    return;
}

    resultsList.innerHTML = "";

    data.forEach(piece => {
        const li = document.createElement("li");
        li.classList = "list-group-item d-flex justify-content-between align-items-center border-start-0 border-end-0"

        const textDiv = document.createElement("div");
        textDiv.innerHTML= `
            <strong> ${piece.title}</strong> <br>
            <span class="text-muted">${piece.composer}</span>
            `;
        const button = document.createElement("button");
        button.classList = "btn btn-sm btn-outline-primary";
        button.textContent ="Add";

        button.onclick = () => addPiece(piece.id);

        li.appendChild(textDiv);
        li.appendChild(button);

        resultsList.appendChild(li);
    });
});
    async function addPiece(pieceId){

        
        try {
            const response = await fetch('/add-piece', {
                method : 'POST',
                headers :{
                    'Content-type':'application/json'
                },
                body : JSON.stringify({'piece_id' : pieceId})
            });
            
            if (response.status === 409) {
                alert("That piece is already in your projects.");
                return;
            }

            else if (response.ok) {
                console.log("piece added to current projects!")
                alert("piece added to current projects!")
            }
            else{
                console.log("failed to add piece");
            }
        } catch (error){
            console.log('Error', error);
        }
    }
