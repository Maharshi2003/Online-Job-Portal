(function () {
    var LOWERCASE_EMAIL = /^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$/;

    function isEmailField(input) {
        if (!input || input.disabled || input.readOnly) return false;
        if (input.classList && input.classList.contains('cb-email-input')) return true;
        if ((input.type || '').toLowerCase() === 'email') return true;
        var name = (input.name || '').toLowerCase();
        if (name === 'email' || name === 'emailid') return true;
        var placeholder = (input.placeholder || '').toLowerCase();
        if (placeholder.indexOf('email') !== -1) return true;
        return false;
    }

    function messageFor(value) {
        if (!value) return '';
        if (/[A-Z]/.test(value)) return 'Email should be in small letters only.';
        if (!LOWERCASE_EMAIL.test(value)) return 'Enter a valid email address.';
        return '';
    }

    function ensureHint(input) {
        var next = input.nextElementSibling;
        if (next && next.classList && next.classList.contains('cb-email-error-msg')) {
            return next;
        }
        var hint = document.createElement('small');
        hint.className = 'cb-email-error-msg';
        hint.setAttribute('aria-live', 'polite');
        input.insertAdjacentElement('afterend', hint);
        return hint;
    }

    function validateInput(input) {
        var value = (input.value || '').trim();
        var msg = messageFor(value);
        var hint = ensureHint(input);
        hint.textContent = msg;
        hint.style.display = msg ? 'block' : 'none';
        input.classList.toggle('cb-email-error', !!msg);
        input.setCustomValidity(msg);
        return !msg;
    }

    function bindInput(input) {
        if (!isEmailField(input) || input.dataset.emailBound === '1') return;
        input.dataset.emailBound = '1';
        input.setAttribute('autocapitalize', 'none');
        input.setAttribute('spellcheck', 'false');
        ['input', 'blur', 'change', 'keyup'].forEach(function (evt) {
            input.addEventListener(evt, function () { validateInput(input); });
        });
        var form = input.form;
        if (form && form.dataset.emailSubmitBound !== '1') {
            form.dataset.emailSubmitBound = '1';
            form.addEventListener('submit', function (e) {
                var fields = form.querySelectorAll('input');
                var ok = true;
                fields.forEach(function (field) {
                    if (isEmailField(field) && !validateInput(field)) {
                        ok = false;
                        field.focus();
                    }
                });
                if (!ok) e.preventDefault();
            });
        }
    }

    function scan(root) {
        (root || document).querySelectorAll('input').forEach(bindInput);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { scan(document); });
    } else {
        scan(document);
    }
})();
