// Exam number: YOO76998

$(document).ready(function () { // avoid polluting the global "namespace"

    // the "browse categories" menu on every page
	$('#category').change(function () {
		if (this.value !== '') {
			$('.browse').submit();
		}
	});


    function getCharacterCount(id) {
        return document.getElementById(id).value.length;
    }

    // short description word count, on any project create/edit page
    if ($('#project_short_description__row .w2p_fc').length) {
        function updateCharacterCountDisplay() {
            var count = getCharacterCount('project_short_description');
            document.getElementById('project_short_description__wordcount').innerHTML = count + ' of 120 characters used';
        }
        $('#project_short_description__row .w2p_fc').append('<div id="project_short_description__wordcount"></div>');
        updateCharacterCountDisplay();
        $('#project_short_description').on('click change keydown keypress keyup blur focus', updateCharacterCountDisplay);
    }

    // credit card
    if ($('#credit_card_number__row .w2p_fc').length) {
        function updateCreditCardLengthDisplay() {
            var count = getCharacterCount('credit_card_number');
            document.getElementById('credit_card_number__wordcount').innerHTML = count + ' of 16 digits';
        }
        $('#credit_card_number__row .w2p_fc').append('<div id="credit_card_number__wordcount"></div>');
        updateCreditCardLengthDisplay();
        $('#credit_card_number').on('click change keydown keypress keyup blur focus', updateCreditCardLengthDisplay);
    }

});
