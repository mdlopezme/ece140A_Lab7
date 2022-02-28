document.addEventListener("DOMContentLoaded", function() {
    dropdown = document.getElementById('dropdown_selection');
    car_image = document.getElementById('car_image')

    fetch('/names')
        .then(response=>response.json())
        .then(function(response){
            for(index in response){
                var opt = document.createElement('option');
                opt.value = response[index];
                opt.innerHTML = response[index];
                dropdown.appendChild(opt);
            }
        })
        .then( function (){
            console.log(dropdown.value)
            car_image.src = 'images/' + dropdown.value
            car_image.alt = dropdown.value
        }
        )
});