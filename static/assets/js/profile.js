console.log("pipo")
const nom=document.getElementById("id_nom")
const prenom=document.getElementById("id_prenom")

const url= window.location.href
$.ajax({
    type : 'GET',
    url : `${url}/veri`,
    success: function(response){
        console.log(response)
        document.getElementsByName("nom")[0].placeholder=response.nom
        document.getElementsByName("prenom")[0].placeholder=response.prenom
        
    },
    error : function(error){
        console.log(error)
    }
})
