document.getElementById("accounts").addEventListener("click", function () { jumpTo("accounts_section") }, false);
document.getElementById("video").addEventListener("click", function () { jumpTo("types_section") }, false);
document.getElementById("create_page").addEventListener("click", function () { jumpTo("create_page_section") }, false);
document.getElementById("sharing").addEventListener("click", function () { jumpTo("sharing_scrapbook") }, false);
document.getElementById("recov").addEventListener("click", function () { jumpTo("account_recovery") }, false);

function jumpTo(section) {
    document.getElementById(section).scrollIntoView({ behavior: 'smooth' });
}