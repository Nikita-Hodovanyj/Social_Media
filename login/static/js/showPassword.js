
function showRegPassword(img){
  
    let inputId = img.getAttribute('id');
    let input = document.getElementById(inputId);
    

    if (input.type === 'password') {
        input.type = 'text';
        img.src = "/static/images/open-eye.png";
    } else {
        input.type = 'password';
        img.src = "/static/images/eye2.png";
    }


    if(inputShow.type == 'password'){
        inputShow.type = 'text';
        InputImage.src  = "/static/images/open-eye.png"

    }

    else{
        inputShow.type = 'password';
        InputImage.src  = "/static/images/eye2.png"

    }
}

function showAuthPassword(event){
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


document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll('.code-input');

    inputs.forEach((input, index) => {
        input.addEventListener('input', () => {
            const value = input.value;
            if (value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value === '' && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });
});