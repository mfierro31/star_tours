// Getting today's date and setting that date as the min value for all datepickers

let today = new Date();
let dd = today.getDate();
// In JS, months start at 0, so we have to add 1 to all of them
let mm = today.getMonth() + 1;
let yyyy = today.getFullYear();

// In JS, months and days are not 0-padded, so we have to manually add the 0s ourselves
if (dd < 10) {
  dd = '0' + dd;
}

if (mm < 10) {
  mm = '0' + mm;
}

today = `${yyyy}-${mm}-${dd}`;
$('.datepicker').attr('min', today);

// Clear date value from datepicker, in case user doesn't want to pick a flight or a tour after all
$('.container').on("click", ".clear-link", function () {
  // prev() selects the element immediately before the "Clear" link, which is our datepicker input box
  $(this).prev().val("");
  // Have to manually trigger a change here, otherwise the logic below for date min and max changing won't work
  $(this).prev().change();
});

// If depart date is picked, all other datepickers' min dates should be the depart date
$('#depart-date').change(function() {
  if ($('#depart-date').val()) {
    // Unless tour date is already present, then return date's min should be the tour date, since it's always going to be the
    // same or later than the depart date
    if ($('#tour-date').val()) {
      $('#return-date').attr('min', $('#tour-date').val());
    } else {
      $('#return-date').attr('min', $('#depart-date').val());
    }

    $('#tour-date').attr('min', $('#depart-date').val());
  } else {
    // If depart date is empty, then if tour date is present, set return date's min to tour date, otherwise, make the min for
    // both today.
    if ($('#tour-date').val()) {
      $('#return-date').attr('min', $('#tour-date').val());
    } else {
      $('#return-date').attr('min', today);
    }

    $('#tour-date').attr('min', today);
  }
});

// If return date is picked, tour date and depart date's max must be return date's date
$('#return-date').change(function() {
  if ($('#return-date').val()) {
    $('#depart-date').attr('max', $('#return-date').val());
    $('#tour-date').attr('max', $('#return-date').val());
  } else {
    // Unless tour date is present, then depart date's max should be tour date
    if ($('#tour-date').val()) {
      $('#depart-date').attr('max', $('#tour-date').val());
    } else {
      $('#depart-date').attr('max', '');
    }

    $('#tour-date').attr('max', '');
  }
});

// If tour date is picked, then depart date's max and return date's min should be the tour date
$('#tour-date').change(function() {
  if ($('#tour-date').val()) {
    $('#depart-date').attr('max', $('#tour-date').val());
    $('#return-date').attr('min', $('#tour-date').val());
  } else {
    // Unless return date is present, then depart date's max should be return date
    if ($('#return-date').val()) {
      $('#depart-date').attr('max', $('#return-date').val());
    } else {
      $('#depart-date').attr('max', '');
    }
    // Unless depart date is present, then return date's min should be depart date
    if ($('#depart-date').val()) {
      $('#return-date').attr('min', $('#depart-date').val());
    } else {
      $('#return-date').attr('min', today);
    }
  }
});

// Adding parts to our form that can only show up after a user has picked something

// Getting tours for a particular planet when that particular planet is selected
async function getTours() {
  $('#tour').empty();
  
  const $planet = $('#planet').val();
  const resp = await axios.get(`/tours/${$planet}`);

  for (tour of resp.data.tours) {
    $('#tour').append(`<option value="${tour.id}">
                        ${tour.name}
                        |
                        Start: ${tour.start_time}
                        |
                        End: ${tour.end_time}
                        |
                        Duration: ${tour.duration}
                        |
                        Price: $${tour.price}
                      </option>`);
  }

  $('#tour').append('<option value="0">None</option>');
};

// Getting the flights for a particular planet when that planet is selected
async function getFlights() {
  $('.flight').empty();

  const $planet = $('#planet').val();
  const resp = await axios.get(`/flights/${$planet}`);

  for (flight of resp.data.flights) {
    if (flight.arrive_planet === $planet) {
      $('#depart-flight').append(`
      <option value="${flight.num}">
        ${flight.num}: ${flight.depart_planet} to ${flight.arrive_planet} 
        | 
        Takeoff: ${flight.depart_time} 
        | 
        Arrive: ${flight.arrive_time}
        |
        Duration: ${flight.flight_time}
        |
        Price: $${flight.price}
      </option>
      `);
    } else if (flight.depart_planet === $planet) {
      $('#return-flight').append(`
      <option value="${flight.num}">
        ${flight.num}: ${flight.depart_planet} to ${flight.arrive_planet} 
        | 
        Takeoff: ${flight.depart_time} 
        | 
        Arrive: ${flight.arrive_time}
        |
        Duration: ${flight.flight_time}
        |
        Price: $${flight.price}
      </option>
      `);
    }
  }

  $('.flight').append('<option value="0">None</option>');
}

function clearFlightOrTour(thing) {
  // Function to clear out the flight, date, and tour fields when their checkboxes are checked
  if (thing === "departFlight") {
    if ($('#no_depart').prop('checked')) {
      $('#depart-flight').val('0');
      $('#depart-date').val('');
      // Have to manually trigger a change for these values, otherwise other functionality won't work.
      $('#depart-date').change();
      $('#depart-flight').prop('disabled', true);
      $('#depart-date').prop('disabled', true);
    } else {
      $('#depart-flight').prop('disabled', false);
      $('#depart-date').prop('disabled', false);
    }
  }

  if (thing === "returnFlight") {
    if ($('#no_return').prop('checked')) {
      $('#return-flight').val('0');
      $('#return-date').val('');
      $('#return-date').change();
      $('#return-flight').prop('disabled', true);
      $('#return-date').prop('disabled', true);
    } else {
      $('#return-flight').prop('disabled', false);
      $('#return-date').prop('disabled', false);
    }
  }

  if (thing === "tour") {
    if ($('#no_tour').prop('checked')) {
      $('#tour').val('0');
      $('#tour-date').val('');
      $('#tour-date').change();
      $('#tour').prop('disabled', true);
      $('#tour-date').prop('disabled', true);
    } else {
      $('#tour').prop('disabled', false);
      $('#tour-date').prop('disabled', false);
    }
  }
}

async function addTour() {
  // First, remove any previous alerts
  $('.alert').remove();

  // Secondly, declare our variables and check to see if any of the flights & dates or tour & date are missing values.  If they
  // are, manually check their associated no flight/no tour checkbox
  let noDepart;
  let noReturn;
  let noTour;
  const $tourId = parseInt($('#tour').val());
  const $tourDate = $('#tour-date').val();
  const $departFlightDate = $('#depart-date').val();
  const $returnFlightDate = $('#return-date').val();
  const $departFlightId = parseInt($('#depart-flight').val());
  const $returnFlightId = parseInt($('#return-flight').val());
  const $planetName = $('#planet').val();

  if (!$tourId || !$tourDate) {
    $('#no_tour').prop('checked', true);
    $('#no_tour').change();
  }

  if (!$departFlightId || !$departFlightDate) {
    $('#no_depart').prop('checked', true);
    $('#no_depart').change();
  }

  if (!$returnFlightId || !$returnFlightDate) {
    $('#no_return').prop('checked', true);
    $('#no_return').change();
  }

  // Now, check to see which checkboxes are checked and assign their variables values
  if ($('#no_depart').prop('checked')) {
    noDepart = true;
  } else {
    noDepart = false;
  }

  if ($('#no_return').prop('checked')) {
    noReturn = true;
  } else {
    noReturn = false;
  }

  if ($('#no_tour').prop('checked')) {
    noTour = true;
  } else {
    noTour = false;
  }

  requestObj = {
    tourId: $tourId,
    tourDate: $tourDate,
    departFlightDate: $departFlightDate,
    returnFlightDate: $returnFlightDate,
    departFlightId: $departFlightId,
    returnFlightId: $returnFlightId,
    planetName: $planetName,
    noDepart: noDepart,
    noReturn: noReturn,
    noTour: noTour
  };

  const resp = await axios.post('/itineraries/add/tour', requestObj);

  if (resp.data.msg === "Successfully added tour to user's itinerary.") {
    // add a new tour field/planet field and disable the tour/planet field before it as well as deleting its ID and name, so that 
    // its info is not received in the final submit of the form.

    // Remove previous dates/times of flights
    $('.depart-arrive-datetimes').remove();

    // Remove 'clear' links as well for the previous date pickers.  You can still clear the previous dates if you click on the 
    //'clear' links, even though the input boxes are disabled
    $('.clear-link').remove();

    // First, disable all previous inputs, except for our submit button, which is in fact, an input type
    $('form :input:not([id=submit-trip-btn])').prop('disabled', true);

    // To help the user remember the dates and times of the tours and flights they chose, we can display them below each one
    $(`
    <p>Start Date/Time: ${resp.data.tour_start_datetime}</p>
    <p>End Date/Time: ${resp.data.tour_end_datetime}</p>
    <p>Price: $${resp.data.tour_price}</p>
    `).insertAfter('#tour-date');

    if (resp.data.departure_datetime && resp.data.arrival_datetime && resp.data.d_flight_price) {
      $(`
      <p class="depart-arrive-datetimes">Depart Date/Time: ${resp.data.departure_datetime}</p>
      <p class="depart-arrive-datetimes">Arrival Date/Time: ${resp.data.arrival_datetime}</p>
      <p class="depart-arrive-datetimes">Price: $${resp.data.d_flight_price}</p>
    `).insertAfter('#depart-flight');
    }

    if (resp.data.return_datetime && resp.data.return_arrival_datetime && resp.data.r_flight_price) {
      $(`
      <p class="depart-arrive-datetimes">Depart Date/Time: ${resp.data.return_datetime}</p>
      <p class="depart-arrive-datetimes">Arrival Date/Time: ${resp.data.return_arrival_datetime}</p>
      <p class="depart-arrive-datetimes">Price: $${resp.data.r_flight_price}</p>
    `).insertAfter('#return-flight');
    }

    // Then, remove all the previous tour inputs' unique attributes so we can use those same unique attributes for our new inputs
    $('#tour-label').removeAttr('for');
    $('#tour-label').removeAttr('id');
    $('#tour').removeAttr('name');
    $('#tour').removeAttr('id');

    $('#tour-date-label').removeAttr('for');
    $('#tour-date-label').removeAttr('id');
    $('#tour-date').removeAttr('name');
    $('#tour-date').removeAttr('id');

    $('#no_tour').removeAttr('name');
    $('#no_tour').removeAttr('id');
    $('#no_tour_label').removeAttr('for');
    $('#no_tour_label').removeAttr('id');

    //Finally, insert new tour inputs with previous unique attributes
    $(`
    <div class="form-row justify-content-center my-4">
      <div class="col-11 col-sm-5 col-md-3">
        <div class="form-group text-center">
          <label for="tour" id="tour-label">Tour</label>
          <select class="form-control" id="tour" name="tour">
          
          </select>
        </div>
        <div class="form-group text-center form-check">
          <input class="form-check-input" id="no_tour" name="no_tour" onchange="clearFlightOrTour('tour');" type="checkbox" value="y">
          <label class="form-check-label" for="no_tour" id="no_tour_label">No Tour</label>
        </div>
      </div>
    </div>
    
    <div class="form-row justify-content-center">
      <div class="col-11 col-sm-5 col-md-3">
        <div class="form-group text-center">
          <label for="tour_date" id="tour-date-label">Tour Date</label>
          <input class="form-control datepicker mb-3" id="tour-date" name="tour_date" type="date">        
          <a class="clear-link" id="tour-date-clear" href="javascript:void();">Clear</a>
        </div>
      </div>
    </div>
    <hr>`).insertBefore('#warning-msg');

    // We also have to set all the dynamic attributes, like min and max for the datepicker
    $('#tour-date').attr('min', today);

    if ($('#depart-date').val()) {
      $('#tour-date').attr('min', $('#depart-date').val());
    }

    if ($('#return-date').val()) {
      $('#tour-date').attr('max', $('#return-date').val());
    }

    // And we have to manually call getTours() again, otherwise our new tour selection box won't get populated
    getTours();
  } else {
    // If something goes wrong, we insert an alert right above the 'add another tour' or 'add another planet' link
    $(`<div class="alert alert-danger mt-3">${resp.data.msg}</div>`).insertBefore("#add-xtra-tour-link");
  }
}

function changeFormInputs() {
  const $tourId = parseInt($('#tour').val());
  const $tourDate = $('#tour-date').val();
  const $departFlightDate = $('#depart-date').val();
  const $returnFlightDate = $('#return-date').val();
  const $departFlightId = parseInt($('#depart-flight').val());
  const $returnFlightId = parseInt($('#return-flight').val());

  if (!$tourId || !$tourDate) {
    if ($('#no_tour').prop('disabled', false)) {
      $('#no_tour').prop('checked', true);
      $('#no_tour').change();
    }
  }

  if (!$departFlightId || !$departFlightDate) {
    if ($('#no_depart').prop('disabled', false)) {
      $('#no_depart').prop('checked', true);
      $('#no_depart').change();
    }
  }

  if (!$returnFlightId || !$returnFlightDate) {
    if ($('#no_return').prop('disabled', false)) {
      $('#no_return').prop('checked', true);
      $('#no_return').change();
    }
  }
}

async function addUpTotal() {
  const $noDepart = $('#no_depart').prop('checked');
  const $noReturn = $('#no_return').prop('checked');
  const $noTour = $('#no_tour').prop('checked');
  const $departId = parseInt($('#depart-flight').val());
  const $returnId = parseInt($('#return-flight').val());
  const $tourId = parseInt($('#tour').val());

  const requestObj = {
    noDepart: $noDepart,
    noReturn: $noReturn,
    noTour: $noTour,
    departId: $departId,
    returnId: $returnId,
    tourId: $tourId
  };

  const resp = await axios.post('/itineraries/total', requestObj);

  $('#total-amt').text(`$${resp.data.total}`);
}

function unDisable() {
  $(':disabled').prop('disabled', false);
}

function bookFormSubmit() {
  $('#book-form').submit();
}

// On page load for our book page, load all the tours and flights for the selected planet
$(document).ready(function() {
  $('#planet').change();
});