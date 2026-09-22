/**
 *
 * -----------------------------------------------------------------------------
 *
 * Template : Virtuo Personal Portfolio HTML Template
 * Author : themes-park
 * Author URI : https://themes-park.com/ 
 *
 * -----------------------------------------------------------------------------
 *
 **/

(function ($) {
    'use strict';

    var form = $('#contact-form');
    var formMessages = $('#form-messages');

    // Remove error highlights on input
    $(form).on('input change', '.input-field', function () {
        $(this).removeClass('input-error');
    });

    // Real-time phone input filter: ONLY allow digits 0-9 and strictly cap at 10 digits
    $('#contact-phone').on('input keydown keyup paste', function () {
        var self = this;
        setTimeout(function () {
            var cleaned = $(self).val().replace(/\D/g, '');
            if (cleaned.length > 10) {
                cleaned = cleaned.substring(0, 10);
            }
            $(self).val(cleaned);
        }, 0);
    });

    // Real-time message length counter and 500-char cap
    $('#contact-message').on('input keyup paste', function () {
        var self = this;
        setTimeout(function () {
            var text = $(self).val();
            if (text.length > 500) {
                text = text.substring(0, 500);
                $(self).val(text);
            }
            $('#msg-count').text(text.length);
        }, 0);
    });

    // Set up an event listener for the contact form.
    $(form).submit(function (e) {
        e.preventDefault();

        // Remove existing error classes
        $('.input-field').removeClass('input-error');

        var nameInput = $('#contact-name');
        var phoneInput = $('#contact-phone');
        var emailInput = $('#contact-email');
        var messageInput = $('#contact-message');

        var name = nameInput.val() ? nameInput.val().trim() : '';
        var phone = phoneInput.val() ? phoneInput.val().trim() : '';
        var email = emailInput.val() ? emailInput.val().trim() : '';
        var message = messageInput.val() ? messageInput.val().trim() : '';

        // --- STRICT CLIENT-SIDE VALIDATION ---
        // 1. Name Check
        if (name.length < 2) {
            showError('Please enter your full name (at least 2 characters).', nameInput);
            return false;
        }

        // 2. Phone Check (strictly 10 digits only)
        var cleanPhone = phone.replace(/\D/g, '');
        if (!cleanPhone || cleanPhone.length !== 10) {
            showError('Please enter a valid 10-digit phone number (exactly 10 digits).', phoneInput);
            return false;
        }

        // 3. Email Check (strict format with complete domain)
        var emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!email || !emailRegex.test(email)) {
            showError('Please enter a complete and valid email address (e.g., name@gmail.com).', emailInput);
            return false;
        }

        // 4. Message Check (minimum 10, maximum 500 characters)
        if (message.length < 10) {
            showError('Please enter a meaningful message of at least 10 characters.', messageInput);
            return false;
        }
        if (message.length > 500) {
            showError('Message cannot exceed 500 characters.', messageInput);
            return false;
        }

        // Helper function to display errors
        function showError(msg, elementToFocus) {
            $(formMessages).removeClass('success').addClass('error').text(msg).fadeIn(200);
            if (elementToFocus && elementToFocus.length) {
                elementToFocus.addClass('input-error').focus();
            }
        }

        var submitBtn = $(form).find('#submit');
        var btnText = submitBtn.find('.btn-text');
        var originalBtnText = btnText.text();

        // Loading state
        submitBtn.prop('disabled', true);
        btnText.text('Sending Message...');

        // Serialize the form data.
        var formData = $(form).serialize();

        // Submit the form using AJAX.
        $.ajax({
            type: 'POST',
            url: $(form).attr('action'),
            data: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .done(function (response) {
            $(formMessages).removeClass('error').addClass('success').text('Thank you! Your message has been sent successfully. Refreshing page...').fadeIn(200);

            if ($(form)[0]) {
                $(form)[0].reset();
            }
            $('#contact-name, #contact-email, #contact-phone, #subject, #contact-message').val('');

            btnText.text('Message Sent! Refreshing...');

            // Auto-refresh after 1.8 seconds as requested
            setTimeout(function () {
                window.location.reload();
            }, 1800);
        })
        .fail(function (data) {
            $(formMessages).removeClass('success').addClass('error').fadeIn(200);

            if (data.responseText && data.responseText.trim() !== '') {
                $(formMessages).text(data.responseText);
            } else {
                $(formMessages).text('Oops! An error occurred and your message could not be sent. Please check your inputs and try again.');
            }

            btnText.text(originalBtnText);
            submitBtn.prop('disabled', false);
        });
    });

})(jQuery);
