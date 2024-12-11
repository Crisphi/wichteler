document.addEventListener("DOMContentLoaded", function() {
    let menuToggle = document.getElementById('toggle-sidebar');
    let sidebar = document.querySelector('.sidebar');
    let menuList = document.querySelectorAll('.menu-items li');

    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });

    function activeLink() {
        menuList.forEach(item => item.classList.remove('active'));
        this.classList.add('active');
    }

    menuList.forEach(item => item.addEventListener('click', activeLink));
});



const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const registerlogincontainer = document.querySelector(".register-login-container");
const sign_in_btn2 = document.querySelector("#sign-in-btn2");
const sign_up_btn2 = document.querySelector("#sign-up-btn2");
sign_up_btn.addEventListener("click", () => {
    registerlogincontainer.classList.add("sign-up-mode");
});
sign_in_btn.addEventListener("click", () => {
    registerlogincontainer.classList.remove("sign-up-mode");
});
sign_up_btn2.addEventListener("click", () => {
    registerlogincontainer.classList.add("sign-up-mode2");
});
sign_in_btn2.addEventListener("click", () => {
    registerlogincontainer.classList.remove("sign-up-mode2");
});