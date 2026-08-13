(function () {
    "use strict";

    var STORAGE_KEY = "jobportal-theme";
    var root = document.documentElement;

    function getStoredTheme() {
        try {
            return localStorage.getItem(STORAGE_KEY) || "light";
        } catch (e) {
            return "light";
        }
    }

    function applyTheme(theme) {
        if (theme === "dark") {
            root.classList.add("dark-mode");
        } else {
            root.classList.remove("dark-mode");
        }
        syncToggles(theme);
    }

    function syncToggles(theme) {
        var toggles = document.querySelectorAll(".theme-toggle");
        for (var i = 0; i < toggles.length; i++) {
            toggles[i].setAttribute("aria-checked", theme === "dark" ? "true" : "false");
        }
    }

    function setTheme(theme) {
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch (e) {
            /* localStorage unavailable, ignore */
        }
        applyTheme(theme);
    }

    function toggleTheme() {
        setTheme(getStoredTheme() === "dark" ? "light" : "dark");
    }

    /* Apply immediately (before body paints) to avoid a flash of the wrong theme */
    applyTheme(getStoredTheme());

    document.addEventListener("DOMContentLoaded", function () {
        syncToggles(getStoredTheme());

        var toggles = document.querySelectorAll(".theme-toggle");
        for (var i = 0; i < toggles.length; i++) {
            toggles[i].addEventListener("click", toggleTheme);
            toggles[i].addEventListener("keydown", function (e) {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    toggleTheme();
                }
            });
        }
    });
})();
