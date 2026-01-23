const questionButtons = document.querySelectorAll("button.question");
    
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function handleLikeClick(event) {
    const { questionId, likeType } = event.target.dataset;
    const url = `/questions/${questionId}/like/`;
    const data = { type: likeType };

    const init = {
        method: "POST",
        mode: 'same-origin',
        headers: { "X-CSRFToken": csrftoken, 'Content-Type': 'application/json; charset=UTF-8' },
        body: JSON.stringify(data),
    }
    
    fetch(url, init)
        .then((response) => response.json())
        .then((responseAsJson) => {
            const likeCounter = document.querySelector(`span.counter[data-question-id="${questionId}"]`);
            likeCounter.textContent = responseAsJson.new_likes_count
            type = responseAsJson.type
            btnlike = document.querySelector(`button.question[data-question-id="${questionId}"][data-like-type="1"]`);
            btndislike = document.querySelector(`button.question[data-question-id="${questionId}"][data-like-type="0"]`);
            console.log(type)
            if (type=="-1") {
                btndislike.classList.add("chosen")
                btnlike.classList.remove("chosen")
            } else if (type=="0") {
                btndislike.classList.remove("chosen")
                btnlike.classList.remove("chosen")
            } else if (type=="1") {
                btndislike.classList.remove("chosen")
                btnlike.classList.add("chosen")
            }
        })
        .catch((e) => { console.error(e)})
        .finally(() => {console.log("finally")})
}

for (const btn of questionButtons) {
    btn.addEventListener("click", (event) => handleLikeClick(event) );
}
