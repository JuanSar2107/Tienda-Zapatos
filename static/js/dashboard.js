const accountArea = document.querySelector(".account-area");
const accountTrigger = document.querySelector(".account-trigger");

if (accountArea && accountTrigger) {
    accountTrigger.addEventListener("click", () => {
        const isOpen = accountArea.classList.toggle("is-open");
        accountTrigger.setAttribute("aria-expanded", String(isOpen));
    });
}
