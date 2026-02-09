const form = document.getElementById("answer-form");
console.log(userId)

form.addEventListener('submit', async(e) => {
    console.log("Hello")
})

console.log(CENTRIFUGO_URL)
const centrifuge = new Centrifuge(`ws://${CENTRIFUGO_URL}/connection/websocket`, { token: CENTRIFUGO_TOKEN })

centrifuge.on('connecting', function (ctx) {
    console.log(`connecting: ${ctx.code}, ${ctx.reason}`);
}).on('connected', function (ctx) {
    console.log(`connected over ${ctx.transport}`);
}).on('disconnected', function (ctx) {
    console.log(`disconnected: ${ctx.code}, ${ctx.reason}`);
}).connect();

console.log(CENTRIFUGO_CHANNEL)
const sub = centrifuge.newSubscription(CENTRIFUGO_CHANNEL);

document.addEventListener('click', function(event) {
    const answerBtn = event.target.closest('.btn-like.answer');
    if (answerBtn) {
        event.preventDefault();
        const { answerId, likeType } = answerBtn.dataset;
        
        const url = `/questions/answers/${answerId}/like/`;
        const data = { type: likeType };
        
        const init = {
            method: "POST",
            mode: 'same-origin',
            headers: { 
                "X-CSRFToken": csrftoken, 
                'Content-Type': 'application/json; charset=UTF-8' 
            },
            body: JSON.stringify(data),
        };
        
        fetch(url, init)
            .then((response) => response.json())
            .then((responseAsJson) => {
                console.log(responseAsJson);
                const likeCounter = document.querySelector(`span.counter[data-answer-id="${answerId}"]`);
                if (likeCounter) {
                    likeCounter.textContent = responseAsJson.new_likes_count;
                }
                
                const type = responseAsJson.type;
                console.log(type);
                const btnlike = document.querySelector(`button.answer[data-answer-id="${answerId}"][data-like-type="1"]`);
                const btndislike = document.querySelector(`button.answer[data-answer-id="${answerId}"][data-like-type="0"]`);
                if (type == "-1") {
                    btndislike?.classList.add("chosen");
                    btnlike?.classList.remove("chosen");
                } else if (type == "0") {
                    btndislike?.classList.remove("chosen");
                    btnlike?.classList.remove("chosen");
                } else if (type == "1") {
                    btndislike?.classList.remove("chosen");
                    btnlike?.classList.add("chosen");
                }
            })
            .catch((e) => { console.error(e); });
    }
    
    const checkbox = event.target.closest('input.checkbox');
    if (checkbox && !checkbox.hasAttribute('disabled')) {
        event.preventDefault();
        const { answerId } = checkbox.dataset;
        
        const url = `/questions/answers/${answerId}/check/`;
        const init = {
            method: "POST",
            mode: 'same-origin',
            headers: { "X-CSRFToken": csrftoken },
        };
        
        fetch(url, init)
            .then((response) => response.json())
            .then((responseAsJson) => {
                checkbox.checked = responseAsJson.is_correct;
            })
            .catch((e) => { console.error(e); });
    }
});

sub
.on('publication', function (ctx) {
    const {message} = ctx.data;
    const { id, content, author, is_liked, likes, is_correct, question_author_id } = message || {};
    
    const answerContainer = document.querySelector(".answers");
    const answerTemplate = document.querySelector(".answer-item.template");
    
    const newAnswer = answerTemplate.cloneNode(true);
    
    newAnswer.querySelector('.avatar').src = author.avatar;
    newAnswer.querySelector('.description').textContent = content;
    
    const elementsWithId = newAnswer.querySelectorAll('[data-answer-id="-1"]');
    elementsWithId.forEach(element => {
        element.dataset.answerId = id;
    });
    
    const likeCounter = newAnswer.querySelector('.counter[data-answer-id="' + id + '"]');
    if (likeCounter) {
        likeCounter.textContent = likes;
    }
    
    const btnLike = newAnswer.querySelector('.btn-like.answer[data-like-type="1"][data-answer-id="' + id + '"]');
    const btnDislike = newAnswer.querySelector('.btn-like.answer[data-like-type="0"][data-answer-id="' + id + '"]');

    const checkbox = newAnswer.querySelector('.checkbox[data-answer-id="' + id + '"]');
    if (checkbox) {
        checkbox.checked = is_correct || false;
    }
    if ("{{ user.is_authenticated}}"=="True" && userId == question_author_id) {
        checkbox.removeAttribute('disabled');
    }
    newAnswer.classList.remove("template");
    
    answerContainer.appendChild(newAnswer);
    
    console.log('New answer added:', message);
})
.on('subscribing', function (ctx) {
    console.log(`subscribing: ${ctx.code}, ${ctx.reason}`);
})
.on('subscribed', function (ctx) {
    console.log('subscribed', ctx);
})
.on('unsubscribed', function (ctx) {
    console.log(`unsubscribed: ${ctx.code}, ${ctx.reason}`);
})
.subscribe();