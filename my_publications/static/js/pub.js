let modal = document.querySelector(".modal-win")
let modalAll = document.querySelector(".modal")
let openModal = document.getElementById("open-modal")
let closeModal = document.querySelector(".close")

openModal.onclick = function() {
  let thoughtText = document.getElementById("thought-input").value;
  if (thoughtText) {
    let textField = document.getElementById("id_text")
    if (textField) {
      textField.value = thoughtText;
    }
  }
  modal.style.display = "block"
  modalAll.style.display = "block"
}

closeModal.onclick = function() {
  modal.style.display = "none"
  modalAll.style.display = "none"

  let form = document.getElementById("publicationForm")
  form.action = "/create/"
  document.querySelector('.title').textContent = "Создание публикации"
  form.reset()
}

document.getElementById("publicationForm")?.addEventListener("submit", function() {
  document.getElementById("thought-input").value = ""
})

document.addEventListener('DOMContentLoaded', function() {
    let dotsButtons = document.querySelectorAll('.dots-button')
    
    dotsButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation()
            let menu = this.nextElementSibling;
            
            document.querySelectorAll('.dropdown-menu.show').forEach(m => {
                if (m !== menu) m.classList.remove('show')
            })
            
            menu.classList.toggle('show')
        })
    })
    
    document.addEventListener('click', function() {
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
            menu.classList.remove('show');
        })
    })
    
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.addEventListener('click', function(e) {
            e.stopPropagation();
        })
    })
})

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault()
        })
    })
})

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.menu-item').forEach(button => {
        button.addEventListener('click', function () {
            if (!this.hasAttribute('data-id')) return

            let postId = this.getAttribute('data-id')

            let form = document.getElementById('publicationForm')
            form.action = `/publications/edit/${postId}/`

            document.querySelector('.title').textContent = "Редагування публікації"

            document.getElementById('id_name').value = this.getAttribute('data-name')
            document.getElementById('id_topic').value = this.getAttribute('data-topic')
            document.getElementById('id_text').value = this.getAttribute('data-text')
            document.getElementById('id_link').value = this.getAttribute('data-link')

            modal.style.display = "block"
            modalAll.style.display = "block"
        })
    })
})



let fileInput = document.getElementById('id_image');
// let modalWIn = document.querySelector('.modal-win')
let fileDiv = document.querySelector('.image-posts');
let trashImage = document.querySelector('.trash-image')

        fileInput.addEventListener('change', (event) => {
            

            let files = event.target.files;
            for (let i = 0; i < files.length; i++) {
                file = files[i];
                console.log(file);
                
            

                let image = document.createElement('img');
                // image.src = {% static 'images/${file.name}'%}
                // Створює посилання на браузері
                image.src = URL.createObjectURL(file);
                image.className = 'image-post';

                let wrapper = document.createElement('div');
                wrapper.className = 'image-wrapper';

                let trashImage = document.createElement('img');
                trashImage.className = 'trash-image';
                trashImage.src = TRASH_IMAGE_SRC
                trashImage.onclick = () => wrapper.remove();

                wrapper.appendChild(image);
                wrapper.appendChild(trashImage);
                fileDiv.appendChild(wrapper);

                
                
            }
            
        });