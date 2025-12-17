if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("static/js/serviceWorker.js")
      .then((res) => console.log("service worker registered"))
      .catch((err) => console.log("service worker not registered", err));
  });
}

const offlineBanner = document.getElementById("offline-banenr");

function updateOnlineStatus() {
  if (navigator.onLine) {
    offlineBanner.style.display = "none";
    console.log("WebApp is online :D");
  } else {
    offlineBanner.style.display = "block";
    console.log("WebApp is offline :[");
  }
}

window.addEventListener("load", updateOnlineStatus);

window.addEventListener("online", function () {
  updateOnlineStatus();
  console.log("Connection lost :[");
});

// This script toggles the active class and aria-current attribute on the nav links
document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll(".nav-link");
  const currentUrl = window.location.pathname;

  navLinks.forEach((link) => {
    const linkUrl = link.getAttribute("href");
    if (linkUrl === currentUrl) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    }
  });
});
