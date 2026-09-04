const accountTrigger = document.querySelector(".account-trigger");
const accountMenu = document.querySelector(".account-menu");

if (accountTrigger && accountMenu) {
    accountTrigger.addEventListener("click", () => {
        const isOpen = !accountMenu.hasAttribute("hidden");
        accountTrigger.setAttribute("aria-expanded", String(!isOpen));
        accountMenu.toggleAttribute("hidden", isOpen);
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".top-user")) {
            accountTrigger.setAttribute("aria-expanded", "false");
            accountMenu.setAttribute("hidden", "");
        }
    });
}
