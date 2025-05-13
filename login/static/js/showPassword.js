
function showPassword(event){
    event.preventDefault(); // щоб форма не відправлялас
    let inputShow = document.getElementById("password");
    let InputImage = document.querySelector(".eye")

    if(inputShow.type == 'password'){
        inputShow.type = 'text';
        InputImage.src  = "/static/images/open-eye.png"

    }

    else{
        inputShow.type = 'password';
        InputImage.src  = "/static/images/eye2.png"

    }


}