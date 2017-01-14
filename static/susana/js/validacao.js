/**
 * Arquivo com função de validação de inscrição estadual, caso seja necessária.
 */

// verifica se a ie eh valida
function checa_ie(ie, cnpj, uf, contribuinte) {
    // verifica se eh contribuinte
    if (contribuinte) {
        // checa a ie e retorna
        return inscricaoEstadual(ie, uf.toLowerCase()) == true;
    }

    // verifica se realmente eh cnpj
    cnpj = so_numeros(cnpj);

    // verifica o tamanho
    if (cnpj.length == 14) { // realmente eh cnpj
        // checa a ie
        return inscricaoEstadual(ie, uf.toLowerCase()) == true;
    }
    
    // retorna null, indicando que nao eh ie
    return null;
}
