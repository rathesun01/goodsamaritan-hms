function create_new_forms(empty_form_id, form_div, div_to_populate){
    var ele = document.getElementById(empty_form_id);
    var clone = ele.cloneNode(true);
    var form_count = document.getElementsByClassName(form_div).length;
    clone.setAttribute('class', form_div);
    clone.setAttribute('id', `form-${form_count}`);
    document.getElementById(div_to_populate).append(clone);
    const regex = new RegExp('__prefix__', 'g');
    clone.innerHTML = clone.innerHTML.replace(regex, form_count);
    var total_forms_ele = document.getElementById('id_form-TOTAL_FORMS');
    console.log(form_count);
    total_forms_ele.setAttribute('value', form_count + 1);
}