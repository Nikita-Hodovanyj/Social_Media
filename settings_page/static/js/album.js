let fileInputs = document.querySelectorAll('.input-photo-class')
let avatarInput = document.getElementById('image-avatar');
// let avatarInput = document.getElementById('image-avatar');
// let avatarFile = document.querySelector('.profile-avatar');
let toogleButtons = document.querySelectorAll(".icon-button")
let image = document.querySelector(".image-album")




toogleButtons.forEach((button) => {
    button.addEventListener("click", (event) =>{
        let albumId = button.id.split('-')[1]
        
        let fileDiv = document.getElementById(`albums-images-${albumId}`);

        if(fileDiv.style.display == "none"){
            fileDiv.style.display = "flex"
            console.log('hide')

        }
        else {
            fileDiv.style.display = "none"
            console.log('show')

        }
    })  

})


fileInputs.forEach((fileInput) => {
    fileInput.addEventListener('change', (event) => {
        event.preventDefault();
        
        console.log('form submit');
        fileInput.form.submit();
        
    });
});


avatarInput.addEventListener('change', (event) => {
        avatarInput.form.submit();
});
