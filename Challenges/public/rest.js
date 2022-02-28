document.addEventListener("DOMContentLoaded", function() {
    dropdown = document.getElementById('dropdown_selection');
    fetch('/names')
        .then(response=>response.json())
        .then(function(response){
            for(index in response){
                var opt = document.createElement('option');
                opt.value = index;
                opt.innerHTML = response[index];
                dropdown.appendChild(opt);
            }
        })
});