console.log("nikie")
const url = window.location.href
console.log(url)
const section= document.querySelector('.container')
console.log(section)

$.ajax({
    type: 'GET',
    url : `${url}search `,
    success: function(response){
        console.log(response.jouer)
        if(response.status ==='disponible'){
            if(response.jouer === 'False'){
                section.innerHTML+=`
                <div class="alert alert-warning alert-dismissible fade show" role="alert">
                    <strong>Salut!! </strong>Vous avez des  quizs  du jour disponible!.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>          
                `
            }else{
            }
        }else{
        }
    },
    error : function(error){
    }
})