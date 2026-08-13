(function () {
    function bindPasswordToggles(root) {
        (root || document).querySelectorAll('.cb-password-toggle').forEach(function (btn) {
            if (btn.dataset.bound === '1') return;
            btn.dataset.bound = '1';
            btn.addEventListener('click', function () {
                var field = btn.closest('.cb-password-field');
                var input = field && field.querySelector('input');
                var icon = btn.querySelector('i');
                if (!input || !icon) return;

                var show = input.type === 'password';
                input.type = show ? 'text' : 'password';
                icon.classList.toggle('fa-eye', !show);
                icon.classList.toggle('fa-eye-slash', show);
                btn.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
                btn.setAttribute('title', show ? 'Hide password' : 'Show password');
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { bindPasswordToggles(document); });
    } else {
        bindPasswordToggles(document);
    }
})();
