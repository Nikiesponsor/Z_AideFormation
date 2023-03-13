const url2= window.location.href
const quizBox= document.getElementById("check")
const quizform= document.getElementById("quiz-form")
const csrf = document.querySelector("[name=csrfmiddlewaretoken]")
const bodyquestion=document.querySelector(".body-question")
const scorebox =document.getElementById("score-box")
const resultbox =document.getElementById("resultbox")
const timerBox = document.getElementById("timer")
const f= document.querySelector('.question')
const boton=document.querySelector('.botom')
console.log(boton)
console.log(url2)



// ----------------implemention des questions-----------------------------
$.ajax({
    type :'GET',
    url : `${url2}data`,
    success: function(response){
        const data = response.data 
        console.log(response.temps)
        comptArebour(response.temps)
    },
    error: function(error){
        console.log(error)
    }
})


// ------------------------------------------------------------------------------------


// -----ENVOI  DE LA DES SES QUESTION ET RECEPTION RESULTATS-----------------------------

const sendData = () =>{
    const element = [...document.getElementsByClassName("ans")]
    const data ={}
    data['csrfmiddlewaretoken'] = csrf.value
    element.forEach(el => {
        if(el.checked){
            data[el.name] = el.value 
        }else{
            if(!data[el.name]){
                data[el.name]=null
            }
        }
    })
    console.log(data)
    $.ajax({
        type : 'POST',
        url : `${url2}save`,
        data: data,
        success : function(response){
            console.log(response)          
        },
        error : function(error){
            console.log(error)            
        }        
    })
    
}


quizform.addEventListener('submit', (e)=>{
    quizform.classList.add('start')
    // e.preventDefault()
    // sendData()
})



//----------------- COMPTE A REBOUR POUR LE TEST--------------------------------
const comptArebour = (time) =>{    
    // console.log(time.toString().length)
    if (time.toString().length < 2){
        timerBox.innerHTML = `<b>0${time}:00 </b>`

    }else{
        timerBox.innerHTML = `<b>${time}:00 </b>`
    }
    let minute = time - 1
    let seconde = 60
    let affichageMinute
    let affichageSeconde
    const timer = setInterval(()=>{
        seconde --
        if( seconde < 0){
            seconde = 59
            minute --
        }
        if(minute.toString().length < 2){
            affichageMinute = '0'+ minute

        }else{
            affichageMinute = minute
        }
        if(seconde.toString().length < 2){
            affichageSeconde = '0'+ seconde
        }else{
            affichageSeconde =seconde
        }
        if(minute === 0 && seconde === 0){
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout( () =>{
                clearInterval(timer)
                if(quizform.classList.contains('start')){
                    swal({
                        title:"Temps expiré",
                        text:"Veuillez actualiser la page pour recommencer",
                        icon:"success"
                     });
                     boton.classList.add("d-none")


                }else{
                    swal({
                        title:"Temps expiré",
                        text:"Veuillez actualiser la page pour recommencer",
                        icon:"error",
                        timer: 5000,
                        buttons: false,
                     });
                     boton.classList.add("d-none")
                    // sendData()
                }                              
            },500)
        }
        timerBox.innerHTML = `<b> ${affichageMinute}:${affichageSeconde} </b>`
    },1000)
}
// ------------------------------------------------------------











