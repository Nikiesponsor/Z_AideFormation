// const heart= document.querySelectorAll(".bxs-heart")
const form = document.querySelectorAll("form")
// const csrf = document.querySelector("[name=csrfmiddlewaretoken]")
const url = window.location.href
const element = [...document.getElementsByClassName("fav")]
const icons= [...document.getElementsByClassName("icons")] 
console.log(url)
icons.forEach(icon =>{
    

})

element.forEach(el =>{
        el.addEventListener('click', (e) =>{
        console.log(e.target.value)
        matiere=e.target.value
        $.ajax({
            type : 'GET',
            url : `${url}/${matiere}/verification`,
            success : function (response) {
                console.log(response.check)
                if(response.check=='supprime'){
                    e.target.classList.replace("bxs-heart","bx-heart")                  
                }else{
                    e.target.classList.replace("bx-heart","bxs-heart")
                }                        
            },
            error : function (error) {
                console.log(error)           
            }
        })
        })       
})






// form.forEach( el =>{
//     el.addEventListener('submit',(e) =>{        
//         user=e.submitter.getAttribute("data-user")
//         matiere=e.submitter.getAttribute("data-Matiere")
//         favoris=e.submitter.getAttribute("data-idfavoris")
//         console.log(favoris)
//         if(favoris ==='None'){
//             favoris=0;
//         }
//         e.preventDefault()
//         console.log(favoris)
//         console.log(e.submitter)
//         $.ajax({
//             type : 'GET',
//             url  : `${url}/${matiere}/${favoris}`,
//             success : function (response) {
//                 console.log(response.fav)
//                 if(response.fav=='del'){
//                     e.submitter.classList.replace("bxs-heart","bx-heart")
//                 }else{
//                     e.submitter.classList.replace("bx-heart","bxs-heart")
//                 }
                
//             },
//             error : function(error) {
//                 console.log(error)
                
//             }

//         })

//     })
// }

// )




