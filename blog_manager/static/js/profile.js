/**
 * NewsBlog — User Profile Management
 * Live image preview for avatar upload and profile form utilities.
 */

(function () {
    'use strict';

    function initProfileAvatarPreview() {
        const avatarInput = document.querySelector('input[type="file"][name="avatar"]');
        const modalPreview = document.getElementById('modalAvatarPreview');
        const profileDisplay = document.getElementById('profileAvatarDisplay');

        if (!avatarInput) return;

        avatarInput.addEventListener('change', function (e) {
            const file = e.target.files && e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function (evt) {
                    const imgHtml = `<img src="${evt.target.result}" class="avatar-img" alt="Avatar Preview">`;
                    if (modalPreview) {
                        modalPreview.innerHTML = imgHtml;
                    }
                    if (profileDisplay) {
                        profileDisplay.innerHTML = imgHtml;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    document.addEventListener('DOMContentLoaded', initProfileAvatarPreview);

})();
