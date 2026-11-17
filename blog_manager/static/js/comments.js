/**
 * NewsBlog — Asynchronous Comments System
 * Handles Create, Inline Edit, and Delete without full page reload.
 */

(function () {
    'use strict';

    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function initComments() {
        const commentList = document.getElementById('commentList');
        const counterEl = document.getElementById('commentsCounter');
        const newCommentForm = document.getElementById('newCommentForm');
        const submitBtn = document.getElementById('submitCommentBtn');
        const submitText = document.getElementById('submitCommentText');
        const formError = document.getElementById('commentFormError');

        function updateCounter(count) {
            if (counterEl) {
                counterEl.textContent = count;
            }
        }

        // 1. Asynchronous Comment Creation
        if (newCommentForm && commentList) {
            newCommentForm.addEventListener('submit', function (e) {
                e.preventDefault();
                const textarea = newCommentForm.querySelector('textarea[name="content"]');
                if (!textarea || !textarea.value.trim()) return;

                if (formError) formError.classList.add('d-none');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    if (submitText) submitText.textContent = 'Posting...';
                }

                const formData = new FormData(newCommentForm);
                const csrfToken = formData.get('csrfmiddlewaretoken');

                fetch(newCommentForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json'
                    }
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Remove empty placeholder if present
                        const placeholder = document.getElementById('emptyCommentsPlaceholder');
                        if (placeholder) placeholder.remove();

                        // Construct avatar markup
                        const avatarMarkup = data.comment.author_avatar
                            ? `<img src="${data.comment.author_avatar}" alt="${escapeHtml(data.comment.author_name)}" class="avatar-img">`
                            : escapeHtml(data.comment.author_initial);

                        // Build new comment card element
                        const newCard = document.createElement('article');
                        newCard.className = 'comment comment--new';
                        newCard.id = `comment-${data.comment.id}`;
                        newCard.dataset.commentId = data.comment.id;

                        newCard.innerHTML = `
                            <header class="comment__head">
                                <span class="comment__avatar">${avatarMarkup}</span>
                                <div class="comment__author">
                                    <span class="comment__name">${escapeHtml(data.comment.author_name)}</span>
                                    <span class="comment__time">
                                        <i class="bi bi-clock"></i> Just now
                                    </span>
                                </div>
                                <div class="comment__actions">
                                    <button type="button"
                                            class="comment__action"
                                            data-bs-toggle="collapse"
                                            data-bs-target="#editComment${data.comment.id}"
                                            aria-expanded="false"
                                            aria-controls="editComment${data.comment.id}">
                                        <i class="bi bi-pencil"></i> Edit
                                    </button>
                                    <form method="POST" action="${data.comment.delete_url}" class="m-0 comment-delete-form" data-comment-id="${data.comment.id}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <button type="submit" class="comment__action comment__action--danger" title="Delete comment">
                                            <i class="bi bi-trash3"></i> Delete
                                        </button>
                                    </form>
                                </div>
                            </header>
                            <div class="comment__body" id="comment-body-${data.comment.id}">
                                ${escapeHtml(data.comment.content).replace(/\n/g, '<br>')}
                            </div>
                            <div class="collapse comment__edit" id="editComment${data.comment.id}">
                                <form method="POST" action="${data.comment.update_url}" class="comment-edit-form" data-comment-id="${data.comment.id}">
                                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                    <textarea name="content" class="comment__edit-textarea" rows="3" required>${escapeHtml(data.comment.content)}</textarea>
                                    <div class="comment__edit-actions">
                                        <button type="button"
                                                class="btn-editorial btn-editorial--sm btn-editorial--ghost"
                                                data-bs-toggle="collapse"
                                                data-bs-target="#editComment${data.comment.id}">
                                            Cancel
                                        </button>
                                        <button type="submit" class="btn-editorial btn-editorial--solid btn-editorial--sm">
                                            <i class="bi bi-check-lg"></i> Save Changes
                                        </button>
                                    </div>
                                </form>
                            </div>
                        `;

                        // Prepend to comment list
                        commentList.prepend(newCard);
                        updateCounter(data.comments_count);
                        textarea.value = '';

                        if (window.showToast) {
                            window.showToast(data.message || 'Comment posted successfully!', 'success');
                        }
                    } else if (data.errors && formError) {
                        formError.querySelector('span').textContent = Object.values(data.errors).flat().join(', ');
                        formError.classList.remove('d-none');
                    }
                })
                .catch(err => {
                    console.error('Comment post error:', err);
                    if (formError) {
                        formError.querySelector('span').textContent = 'An error occurred while posting your comment.';
                        formError.classList.remove('d-none');
                    }
                })
                .finally(() => {
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        if (submitText) submitText.textContent = 'Post Comment';
                    }
                });
            });
        }

        // 2. Asynchronous Comment Editing (Delegated)
        if (commentList) {
            commentList.addEventListener('submit', function (e) {
                const editForm = e.target.closest('.comment-edit-form');
                if (editForm) {
                    e.preventDefault();
                    const commentId = editForm.dataset.commentId;
                    const textarea = editForm.querySelector('textarea[name="content"]');
                    const saveBtn = editForm.querySelector('button[type="submit"]');

                    if (!textarea || !textarea.value.trim()) return;

                    const originalBtnContent = saveBtn ? saveBtn.innerHTML : '';
                    if (saveBtn) {
                        saveBtn.disabled = true;
                        saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Saving...';
                    }

                    fetch(editForm.action, {
                        method: 'POST',
                        body: new FormData(editForm),
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'Accept': 'application/json'
                        }
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.status === 'success') {
                            const bodyEl = document.getElementById(`comment-body-${commentId}`);
                            if (bodyEl) {
                                bodyEl.innerHTML = escapeHtml(data.comment.content).replace(/\n/g, '<br>');
                            }
                            // Close Bootstrap Collapse
                            const collapseEl = document.getElementById(`editComment${commentId}`);
                            if (collapseEl && window.bootstrap) {
                                const bsCollapse = bootstrap.Collapse.getInstance(collapseEl) || new bootstrap.Collapse(collapseEl, { toggle: false });
                                bsCollapse.hide();
                            }
                            if (window.showToast) {
                                window.showToast(data.message || 'Comment updated successfully!', 'success');
                            }
                        } else {
                            if (window.showToast) {
                                window.showToast(data.message || 'Error updating comment.', 'error');
                            } else {
                                alert(data.message || 'Error updating comment.');
                            }
                        }
                    })
                    .catch(err => {
                        console.error('Edit error:', err);
                        if (window.showToast) {
                            window.showToast('Could not update comment.', 'error');
                        }
                    })
                    .finally(() => {
                        if (saveBtn) {
                            saveBtn.disabled = false;
                            saveBtn.innerHTML = originalBtnContent;
                        }
                    });
                }
            });

            // 3. Asynchronous Comment Deletion (Delegated)
            commentList.addEventListener('submit', function (e) {
                const deleteForm = e.target.closest('.comment-delete-form');
                if (deleteForm) {
                    e.preventDefault();
                    if (!confirm('Are you sure you want to delete this comment?')) return;

                    const commentId = deleteForm.dataset.commentId;
                    const commentCard = document.getElementById(`comment-${commentId}`);

                    fetch(deleteForm.action, {
                        method: 'POST',
                        body: new FormData(deleteForm),
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'Accept': 'application/json'
                        }
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.status === 'success') {
                            if (commentCard) {
                                commentCard.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
                                commentCard.style.opacity = '0';
                                commentCard.style.transform = 'translateY(-10px)';
                                setTimeout(() => {
                                    commentCard.remove();
                                    updateCounter(data.comments_count);

                                    // If no comments left, show placeholder
                                    if (data.comments_count === 0 && !document.querySelector('.comment')) {
                                        commentList.innerHTML = `
                                            <div class="empty-state py-4 my-2 comment-empty" id="emptyCommentsPlaceholder">
                                                <div class="empty-state__icon-wrap mb-2" style="width: 50px; height: 50px; font-size: 1.3rem;">
                                                    <i class="bi bi-chat-square-dots"></i>
                                                </div>
                                                <p class="empty-state__text mb-0">
                                                    No comments yet. Be the first to share your perspective!
                                                </p>
                                            </div>
                                        `;
                                    }
                                    if (window.showToast) {
                                        window.showToast(data.message || 'Comment deleted successfully.', 'success');
                                    }
                                }, 250);
                            }
                        } else {
                            if (window.showToast) {
                                window.showToast(data.message || 'Error deleting comment.', 'error');
                            } else {
                                alert(data.message || 'Error deleting comment.');
                            }
                        }
                    })
                    .catch(err => {
                        console.error('Delete error:', err);
                        if (window.showToast) {
                            window.showToast('Could not delete comment.', 'error');
                        }
                    });
                }
            });
        }
    }

    document.addEventListener('DOMContentLoaded', initComments);

})();
