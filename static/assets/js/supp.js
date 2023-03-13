console.log("nikie")
const url = window.location.href
const sup = [...document.getElementsByClassName("supp")]
console.log(url)


sup.forEach(el =>{
    el.addEventListener('click', (e) =>{
        console.log(e.target.value)
        id=e.target.value
        $.ajax({
            type: 'GET',
            url: `${url}/${id}`,
            success: function(response){
                console.log(response)
            },
            error : function(error){
                console.log(error)
            }
        })
    })
})