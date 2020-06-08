
var calendar_options = {
  eventSources: [
  {
    url: '/fpa/api/v1/calendar',
    type: 'GET',
    error: function() {
      $('#script-warning').show();
    }
  }],
  plugins: [ 'dayGrid', 'timeGrid', 'interaction', 'timeGridDay', 'list' ],
  selectable: true,
  aspectRatio: 1.5,
  height: 'auto',
  editable: false,
  navLinks: true,
  eventLimit: true,
  firstDay: 1,
  eventLimitClick: 'popover',
  views: {
    listDay: { buttonText: 'list day' },
    listWeek: { buttonText: 'list week' },
    listMonth: { buttonText: 'list month' }
  },
  header: {
    left: 'prev,next today listDay dayGridMonth',
    center: 'title',
    right: 'prevYear,nextYear'
  },
  navLinkDayClick: function(date, jsEvent) {
    // nothing...
  },
  selectAllow: function(info) {
      return moment().diff(info.start, 'days') <= 0
  },
  dateClick: function(info) {
    click_date(this, info);
  },
  select: function(arg) {
    // nothing to do..
  },
  eventClick: function(info) {
    event_click(this, info);
  },
  eventRender: function (info) {
    var v_br = "<br>";
    var v_owner = "";
    var v_complex = "";

    if (is_not_undefined(info.event.extendedProps.owner)) {
      v_owner = "Owner: " + info.event.extendedProps.owner + v_br;
    }

    if (is_not_undefined(info.event.extendedProps.complex)) {
      v_complex = "Complex: " + info.event.extendedProps.complex + v_br;
    }

    var v_details =
      v_owner + v_complex +
      "Type: " +  info.event.extendedProps.eventType + v_br +
      "Title: " + info.event.title + v_br +
      "Info: " +  info.event.extendedProps.description + v_br +
      "Start: " + moment.parseZone(info.event.start).format("DD-MM-YYYY HH:mm:ss") + v_br +
      "End: " +   moment.parseZone(info.event.end).format("DD-MM-YYYY HH:mm:ss");

    $(info.el).tooltip({ title:v_details, html:true, animation:true, template:ttip_template() });
    info.el.style = info.event.extendedProps.style;

  },
  dayRender: function (dayRenderInfo) {
      //dayRenderInfo.el.innerHTML = "<img src='/static/images/plus.png' width='12' height='12'>";
      //dayRenderInfo.el.innerHTML = "<button type='button' class='btn button_tiny'>Add</button>";
      return dayRenderInfo.el
  }

}

function click_date(cal, info) {  // fired when clicking a calendar date

  // format clicked date to UTC string
  ds=moment.utc(info.dateStr);

  if (moment().diff(ds, 'days') > 0) {
    // if the date is in the past, then return and do no more...
    return;
  }

  // get events in memory
  var arr = cal.getEvents();
  var vdate = moment(ds).format("DD-MM-YYYY");
  var vurl = "/fpa/showdate/" + vdate;

  /////
  show_booking_modal(vurl);
  cal.unselect();
  return;
  /////

}

function show_booking_modal (vurl) {

  $.ajax({url: vurl, success: function(result) {
    $("#model-content-opt").html(result);
  }});

  $("#newBookingModal").modal();
}

function event_click (cal, info) {

  var dateStart = moment(info.event.start).format("DD-MMM-YYYY HH:mm");
  var dateEnd   = moment(info.event.end).format("DD-MMM-YYYY HH:mm");
  $("#bookingTitle").html(info.event.title);
  $("#bookingTitle").css({"background-color": info.el.style.backgroundColor});
  $("#bookingTitle").css({"color": info.el.style.color});
  $("#bookingType").html(info.event.extendedProps.eventType);
  $("#bookingInfo").html(info.event.extendedProps.description);
  if (is_not_undefined(info.event.extendedProps.owner)) {
    v_ar = info.event.extendedProps.owner;
  } else {
    v_ar = "N/A";
  }
  $("#bookingOwner").html(v_ar);
  $("#bookingStart").html(dateStart);
  if (dateEnd == 'Invalid date') {dateEnd=''};
  $("#bookingEnd").html(dateEnd);
  $("#checkBookingModal").modal();
  cal.unselect();

}

// used to override the Bootstrap tooltip template
function ttip_template () {
  return '<div class="tooltip" role="tooltip"><div class="arrow"></div><div class="tooltip-inner bg-white text-left custom_tt_template"></div></div>';
}

// determines if a string is undefined
function is_not_undefined(strg) {
  if (typeof strg == 'undefined') {
    return false;
  } else {
    return true;
  }
}
