export function setErrorShadow(el) {
    el.classList.add("error-shadow");
    const timeout = setTimeout(() => {
        el.classList.remove("error-shadow");
    }, 3000);
    // errorTimeouts.push(timeout)
}
export function setErrorInput(el) {
    el.classList.add("error-border");
    const timeout = setTimeout(() => {
        el.classList.remove("error-border");
    }, 3000);
    // errorTimeouts.push(timeout)
}
