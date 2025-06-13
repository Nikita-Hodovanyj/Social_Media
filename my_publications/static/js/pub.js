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
let fileDiv = document.querySelector('.image-posts');

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    // Создаем DataTransfer для управления файлами
    let dt = new DataTransfer();

    // Добавляем уже существующие файлы из input в dt (если нужно)
    for (let file of files) {
        dt.items.add(file);
    }

    // Очищаем контейнер превью, чтобы не дублировать
    fileDiv.innerHTML = '';

    for (let i = 0; i < dt.items.length; i++) {
        const file = dt.items[i].getAsFile();

        let image = document.createElement('img');
        image.src = URL.createObjectURL(file);
        image.className = 'image-post';

        let wrapper = document.createElement('div');
        wrapper.className = 'image-wrapper';

        let trashImage = document.createElement('img');
        trashImage.className = 'trash-image';
        trashImage.src = TRASH_IMAGE_SRC;

        trashImage.onclick = () => {
            // Удаляем превью
            wrapper.remove();

            // Удаляем файл из DataTransfer
            dt.items.remove(i);
            // Перезаписываем input.files
            fileInput.files = dt.files;
        };

        wrapper.appendChild(image);
        wrapper.appendChild(trashImage);
        fileDiv.appendChild(wrapper);
    }

    // Перезаписываем input.files, на всякий случай
    fileInput.files = dt.files;
});
