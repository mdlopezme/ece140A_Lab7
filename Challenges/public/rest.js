document.addEventListener("DOMContentLoaded", function() {
    dropdown = document.getElementById('dropdown_selection');
    car_image = document.getElementById('car_image')
    plate_plate = document.getElementById('car_plate')
    lincese = document.getElementById('license')

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
            on_change()
        })
});

function on_change(){
    // Create image dector
    fetch('/detect?image='+dropdown.value)
        .then(function(response){
            console.log('Sucess making object: ' + response.url)
        })

    // Set frame parameters
    car_image.src = 'frame?image=' + dropdown.value
    car_image.alt = dropdown.value

    // Set plate parameters
    car_plate.src = 'plate?image=' + dropdown.value
    car_image.alt = dropdown.value

    // Set Plate String
    fetch('/text')
        .then(response=>response.json())
        .then(function(response){
            lincese.innerHTML = response[0]
        })
    
}