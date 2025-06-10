let fileInput = document.getElementById('image-input1');
let fileDiv = document.querySelector('.albums-images');

        fileInput.addEventListener('change', (event) => {
            
            

            let files = event.target.files;
            for (let i = 0; i < files.length; i++) {
                file = files[i];
                console.log(file);
                
            

                let image = document.createElement('img');
                // image.src = {% static 'images/${file.name}'%}
                // Створює посилання на браузері
                image.src = URL.createObjectURL(file);
                image.className = 'image-album';

                let wrapper = document.createElement('div');
                wrapper.className = 'image-wrapper';

                let iconWrapper = document.createElement('div');
                iconWrapper.className = 'icon-wrapper';
                
                let trashImage = document.createElement('img');
                trashImage.className = 'trash-image';
                trashImage.src = TRASH_IMAGE_SRC
                trashImage.onclick = () => wrapper.remove();

                let eyeImage = document.createElement('img');
                trashImage.className = 'trash-image';
                eyeImage.src = EYE_IMAGE_SRC

                wrapper.appendChild(image);
                wrapper.appendChild(iconWrapper);
                iconWrapper.appendChild(trashImage);
                iconWrapper.appendChild(eyeImage);
                fileDiv.appendChild(wrapper);

  
                
            }
            fileInput.value = '';
            
        });