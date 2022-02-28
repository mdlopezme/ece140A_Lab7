document.addEventListener("DOMContentLoaded", function() {
    dropdown = document.getElementById('dropdown_selection');
    car_image = document.getElementById('car_image')
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
        .then(response=>response)
        .then(function(response){
            console.log('Sucess making object: ' + response.url)
        })

    
    car_image.src = 'frame?image=' + dropdown.value
    car_image.alt = dropdown.value
    lincese.innerHTML = 'TEMPLATE'
}