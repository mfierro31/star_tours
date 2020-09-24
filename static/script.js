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
  const resp = await axios.get(`/tours/${$planet}`)

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

  $('#tour').append('<option value="0">None</option>')
};

// Getting the flights for a particular planet when that planet is selected
async function getFlights() {
  $('.flight').empty();

  const $planet = $('#planet').val();
  const resp = await axios.get(`/flights/${$planet}`)

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
      `)
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
      `)
    }
  }

  $('.flight').append('<option value="0">None</option>')
}

// On page load for our book page, load all the tours and flights for the selected planet
$(document).ready(getTours());
$(document).ready(getFlights());