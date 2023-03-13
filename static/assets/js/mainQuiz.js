const modalbtns= document.querySelectorAll(".modal-buton")
const modalbody= document.querySelector(".modal-body")
const btnstar= document.getElementById("star")
const title= document.querySelector(".modal-title")
const url1= window.location.href
console.log(url1)




modalbtns.forEach(modalbtn =>{
    modalbtn.addEventListener('click', ()=>{
        const pk = modalbtn.getAttribute("data-pk")
        const nomquiz=  modalbtn.getAttribute(" data-quizs")
        const matiere = modalbtn.getAttribute("data-matiere")
        const nombreQuestion= modalbtn.getAttribute("data-question")
        const difficulte =modalbtn.getAttribute("data-dificulte")
        const temps=modalbtn.getAttribute("data-time")
        const score = modalbtn.getAttribute("data-score")

        modalbody.innerHTML = ` 
        <div class="h5"> <b>${matiere}</b>  </div>
        <div class="text-muted">
           <ul>
              <li> Niveau du test : <b>${difficulte} </b></li>
              <li> Nombre de question : <b>${nombreQuestion}</b></li>
              <li> Temps : <b>${temps} min </b></li>
              <li> Score minimal pour réussi le test: <b>${score} </b> </li>                      
           </ul>        
        </div> `
        btnstar.addEventListener('click', ()=>{
            window.location.href = url1 + pk
        })

    })
}

)