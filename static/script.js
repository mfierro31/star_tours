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
$('.clear-link').click(function () {
  // prev() selects the element immediately before the "Clear" link, which is our datepicker input box
  $(this).prev().val("");
  // Have to manually trigger a change here, otherwise the logic below for date min and max changing won't work
  $(this).prev().change();
});

// If depart date is picked, all other datepickers' min dates should be the depart date
$('#depart-date').change(function() {
  if ($('#depart-date').val()) {
    $('#return-date').attr('min', $('#depart-date').val());
    $('#tour-date').attr('min', $('#depart-date').val());
  } else {
    $('#return-date').attr('min', today);
    $('#tour-date').attr('min', today);
  }
});

// If return date is picked, tour date and depart date's max must be return date's date
$('#return-date').change(function() {
  if ($('#return-date').val()) {
    $('#depart-date').attr('max', $('#return-date').val());
    $('#tour-date').attr('max', $('#return-date').val());
  } else {
    $('#depart-date').attr('max', '');
    $('#tour-date').attr('max', '');
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
                        Start Time: ${tour.start_time}
                        |
                        End Time: ${tour.end_time}
                        |
                        Duration: ${tour.duration}
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
        Flight ${flight.num}: ${flight.depart_planet} to ${flight.arrive_planet} 
        | 
        Depart Time: ${flight.depart_time} 
        | 
        Arrive Time: ${flight.arrive_time}
        |
        Flight Time: ${flight.flight_time}
      </option>
      `);
    } else if (flight.depart_planet === $planet) {
      $('#return-flight').append(`
      <option value="${flight.num}">
        Flight ${flight.num}: ${flight.depart_planet} to ${flight.arrive_planet} 
        | 
        Depart Time: ${flight.depart_time} 
        | 
        Arrive Time: ${flight.arrive_time}
        |
        Flight Time: ${flight.flight_time}
      </option>
      `);
    }
  }

  $('.flight').append('<option value="0">None</option>');
}

// Adds a tour to the user's itinerary in the database on the backend and adds a new tour and tour_date field
async function addTour() {
  const $tourId = parseInt($('#tour').val());
  const $tourDate = $('#tour-date').val();
  const $departFlightDate = $('#depart-date').val();
  const $returnFlightDate = $('#return-date').val();
  const $departFlightId = parseInt($('#depart-flight').val());
  const $returnFlightId = parseInt($('#return-flight').val());

  request_obj = {
    tourId: $tourId,
    tourDate: $tourDate,
    departFlightDate: $departFlightDate,
    returnFlightDate: $returnFlightDate,
    departFlightId: $departFlightId,
    returnFlightId: $returnFlightId
  };

  const resp = await axios.post('/itineraries/add/tour', request_obj);

  if (resp.data.msg === "Successfully added tour to user's itinerary.") {
    // add a new tour form and disable the tour form before it as well as deleting its ID and name, so that its info is not
    // received in the final submit of the form.
    $('.alert').remove();

    // First, disable the previous tour inputs
    $('#tour').prop('disabled', true);
    $('#tour-date').prop('disabled', true);

    // Then, remove all the previous tour inputs' unique attributes so we can use those same unique attributes for our new inputs
    $('#tour-label').removeAttr('for');
    $('#tour-label').removeAttr('id');
    $('#tour').removeAttr('name');
    $('#tour').removeAttr('id');

    $('#tour-date-label').removeAttr('for');
    $('#tour-date-label').removeAttr('id');
    $('#tour-date').removeAttr('name');
    $('#tour-date').removeAttr('id');

    // Remove 'clear' link as well for the previous date picker.  You can still clear the previous date if you click on it, even
    // though the input box is disabled
    $('#tour-date-clear').remove();

    //Finally, insert new tour inputs with previous unique attributes
    $(`
    <div class="form-row justify-content-center my-4">
      <div class="col-11 col-sm-5 col-md-3">
        <div class="form-group text-center">
          <label for="tour" id="tour-label">Tour</label>
          <select class="form-control" id="tour" name="tour">
          
          </select>
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
    </div>`).insertBefore('#add-tour-container');

    // We also have to set all the dynamic attributes, like min and max for the datepicker
    if ($('#depart-date').val()) {
      $('#tour-date').attr('min', $('#depart-date').val());
    }

    if ($('#return-date').val()) {
      $('#tour-date').attr('max', $('#return-date').val());
    }

    if (!$('#depart-date').val() && !$('#return-date').val()) {
      $('#tour-date').attr('min', today);
    }

    // And we have to manually call getTours() again, otherwise our new tour selection box won't get populated
    getTours();
  } else {
    // If something goes wrong, we insert an alert right above the 'add another tour' link
    $('.alert').remove();
    $(`<div class="alert alert-danger">${resp.data.msg}</div>`).insertBefore("#add-xtra-tour-link");
  }
}

// async function addPlanet() {
  
// }

// On page load for our book page, load all the tours and flights for the selected planet
$(document).ready(getTours());
$(document).ready(getFlights());