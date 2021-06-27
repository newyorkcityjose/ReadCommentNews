// async function handleResponse(card){
//     data = {}
//     div_card = document.getElementById(card.slice(8))
//     console.log(div_card)
//     card.preventDefault()

// $('i.fa-bookmark').on('click', function(event){
//     event.preventDefault();
//     console.log('object')
//     cardId = "#" + $(this).closest("div.media").attr('id');
//     news = $(cardId + " h5.card-title").text();
//     desc = $(cardId + " p.card-text").text();
//     image = $(cardId + " img").attr("src");
//     url = $(cardId + " a.btn").attr("href");
//     data = {
//         "news": news,
//         "desc": desc,
//         "image": image,
//         "url": url
//     };
//     console.log(data);
//     $.ajax({
//         type: "POST",
//         url: "/news",
//         data: data,
//         success: success,
//         dataType: "json"
//     });

// })

// function success(data){
//     console.log(data)
//     if(data.data === "success"){
//         location.reload()
//     }
//     }

    
// }

$('i.fa-bookmark').on('click', function(event){
    event.preventDefault();
    console.log('object')
    cardId = "#" + $(this).closest("div.media").attr('id');
    news = $(cardId + " h5.card-title").text();
    desc = $(cardId + " p.card-text").text();
    image = $(cardId + " img").attr("src");
    url = $(cardId + " a.btn").attr("href");
    data = {
        "news": news,
        "desc": desc,
        "image": image,
        "url": url
    };
    console.log(data);
    $.ajax({
        type: "POST",
        url: "/news/",
        data: data,
        success: success,
        dataType: "json"
    });
})

function success(data){
    console.log(data)
    if(data.data === "success"){
        location.reload()
    }
}

const getDate = () => {
    const date = new Date()
    return date
}

document.addEventListener("DOMContentLoaded", function(event){
    const date = getDate();
    const date_div = document.getElementById("current_date");
    date_div.innerHTML = date.toString().slice(0, 15);
})

const newDate = new Date()
console.log(newDate.getHours())
