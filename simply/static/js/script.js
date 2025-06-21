let closer = document.getElementById('closer')
setTimeout(()=>{
    closer.style.display = 'none'
},3000)





let form = document.getElementById('form')
let pages = document.getElementsByClassName('page')

for(let i = 0; i < pages.length; i++){
  pages[i].addEventListener('click', func)

  function func(e){
    e.preventDefault();

    let page = this.dataset.page

    form.innerHTML += `<input value=${page} name ='page' hidden>`

    form.submit()
  }
}