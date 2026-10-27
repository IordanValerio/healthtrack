document.querySelector("#historico-btn").addEventListener("click", function() {
    document.querySelector("#hide-table").style.display = "block";
});

let visivel = false;

document.querySelector("#historico-btn").addEventListener("click", function() {

    const tabela = document.querySelector("#hide-table");

    if (visivel === false) {
        tabela.style.display = "block";
        document.querySelector("#historico-btn").textContent = "Hide history";
        visivel = true;
    } else {
        tabela.style.display = "none";
        document.querySelector("#historico-btn").textContent = "Show history";
        visivel = false;
    }

});