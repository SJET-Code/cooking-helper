function add_ingredient() {
    var newingredient = document.createElement('span');
    newingredient.innerHTML = '<input type="text" name="ingredient" id="ingredient" placeholder="ingredient name" maxlength="50"> <input type="number" name="amount" id="amount" placeholder="amount" min="1" max="9999999"><input type="text" name="unit" id="unit" placeholder="unit" maxlength="15"><br>';
    document.getElementById('container').appendChild(newingredient);
}

function add_step() {
    var newstep = document.createElement('div');
    newstep.innerHTML = '<textarea name="instructions" id="instruction" form="new" placeholder="add a step" maxlength="100" rows="3" cols="34"></textarea>';
    document.getElementById('instructionsteps').appendChild(newstep);
}
