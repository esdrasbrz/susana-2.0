/**
 * Arquivo com funções de máscaras em js
 */

// retira todos os caracteres que nao sao numericos de uma string
function so_numeros(s) {
    return s.replace(/[^0-9]/g,'');
}

// coloca tudo em maiúsculo em um campo
function to_upper(obj) {
    obj.value = obj.value.toUpperCase();
}

// retira os caracteres nao numericos em um campo
function so_numeros_input(obj) {
    obj.value = so_numeros(obj.value);
}

// retira os caracteres não numéricos e não ',' para fracionario
function so_fracionarios_input(obj) {
    obj.value = obj.value.replace(/[^0-9,]/g,'');
}

// retira os caracteres nao números e letras de um campo
function so_numeros_letras_input(obj) {
    obj.value = obj.value.replace(/[^0-9A-Za-z]/g, '');
}

// verifica se é o enter e submete o botão btSalvar
function on_enter(evt) {
    var key_code = evt.keyCode  ? evt.keyCode  :
                        evt.charCode ? evt.charCode :
                        evt.which    ? evt.which    : void 0;
    
    if (key_code == 13) {
        $("#btSalvar").click();
    }
}
