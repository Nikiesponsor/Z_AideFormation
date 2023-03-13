let toggle =document.querySelector('.toggle')
let body = document.querySelector('body')
const nav =document.querySelector('.header_menu')
const passwords= document.querySelectorAll(".password")
const shows= document.querySelectorAll(".vision")
const navbar= document.querySelector(".navbar");
const icon = document.querySelector(".search-box .bx-search")
const openMenu = document.querySelector(".bx-menu")
const closeMenu =document.querySelector(".bx-x")
const navlink =document.querySelector(".nav-links")




// ------------------------------------
openMenu.addEventListener("click",()=>{
    navlink.style.left="0"
});
closeMenu.addEventListener("click",()=>{
    navlink.style.left="-100%"
})


// icon.addEventListener("click",()=>{
//     navbar.classList.toggle("showinput");
//     if(navbar.classList.contains("showinput")){
//         icon.classList.replace("bx-search","bx-x");
//     }else{
//         icon.classList.replace("bx-x","bx-search");
//     }
// })

shows.forEach( show =>{
    show.addEventListener('click', ()=>{
        passwords.forEach(password =>{
            if(password.type === "password"){
                password.type= "text"
                shows.forEach(icon =>{
                    icon.classList.replace("bxs-hide","bxs-show")
                })
            }else{
                password.type= "password"
                shows.forEach(icon =>{
                    icon.classList.replace("bxs-show","bxs-hide")
                })
            }
        })
    })
})
// ---------------------------------------------
const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }
let backtotop = document.querySelector('.back-to-top')
if (backtotop) {
  const toggleBacktotop = () => {
    
    if (window.scrollY > 100) {
      backtotop.classList.add('active')
    } else {
      backtotop.classList.remove('active')
    }
  }
  window.addEventListener('load', toggleBacktotop)
  onscroll(document, toggleBacktotop)
}

let preloader = document.querySelector('#preloader');
if (preloader) {
  window.addEventListener('load', () => {
    preloader.remove()
  });
}



