console.log("nikiesponsors")
const url = window.location.href
const favoris= [...document.getElementsByClassName("fav")]
console.log(favoris)
// ${url}/${lecon}/fav

favoris.forEach( el =>{
    el.addEventListener('click', (e) =>{
        console.log(e.target.value)
        lecon=e.target.value
        $.ajax({
            type: 'GET',
            url:``,
            success:function(response){
                console.log(response)
                if(response.work === 'supprime'){
                    e.target.classList.replace("bxs-heart","bx-heart")                    
                }else{
                    e.target.classList.replace("bx-heart","bxs-heart")
                }
            },
            error: function(error){
                console.log(error)
            }
        })
    })
} )