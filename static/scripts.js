function add_ingredient() {
    var newingredient = document.createElement('span');
    newingredient.innerHTML = '<input type="text" name="ingredient" id="ingredient" placeholder="ingredient name" maxlength="50"> <input type="text" name="amount" id="amount" placeholder="ingredient amount" maxlength="30"><br>';
    document.getElementById('container').appendChild(newingredient);
}

function add_step() {
    var newstep = document.createElement('div');
    newstep.innerHTML = '<textarea name="instructions" id="instruction" form="new" placeholder="add a step" required maxlength="100" rows="3" cols="34"></textarea>';
    document.getElementById('instructionsteps').appendChild(newstep);
}
