
var calendar_options = {
  eventSources: [
  {
    url: '/fpa/api/v1/calendar',
    type: 'GET',
    error: function() {
      $('#script-warning').show();
    }
  }],
  plugins: [ 'dayGrid', 'timeGrid', 'interaction', 'timeGridDay' ],
  selectable: true,
  aspectRatio: 1.5,
  height: 'auto',
  editable: false,
  navLinks: true,
  eventLimit: true,
  firstDay: 1,
  eventLimit: true,
  eventLimitClick: 'week',
  header: {
    left: 'prev,next today dayGridMonth',
    center: 'title',
    right: 'prevYear,nextYear'
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
    var v_title = info.event.title + "<br/>" + info.event.extendedProps.description + "<br/>Start: " +
        moment.utc(info.event.start).format("DD-MM-YYYY HH:mm:ss") + "<br/>End: " +
        moment.utc(info.event.end).format("DD-MM-YYYY HH:mm:ss");
    $(info.el).tooltip({ title:v_title, html:true, animation:true });
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

  if (!arr.length) { // there are no events shown
    show_booking_modal(cal, ds);
    return;
  }

  var flag = true; // used to record whether any overlapping events are locked
  var title = ""; // holder for title

  // there are events to check
  for (index = 0; index < arr.length; ++index) {

    d1=moment.utc(arr[index].start, "DD-MM-YYYY HH:mm:ss");
    d2=moment.utc(arr[index].end, "DD-MM-YYYY HH:mm:ss");

    if (moment.utc(ds).isSameOrAfter(d1, 'hour') & moment.utc(ds).isSameOrBefore(d2, 'hour')) {
        if (arr[index].extendedProps.locked.toUpperCase() == "NO") {
          // do nothing
        }
        else if (arr[index].extendedProps.locked.toUpperCase() == "YES") {
            flag = false; // we have found at least one event with a locked day matching
            title = arr[index].title;
        }
    } // if

  } // for

  if (flag) {
      show_booking_modal(cal, ds);
      return;
  } else {
      $("#lockedModalLabel").html(title);
      $("#lockedBookingModal").modal();
      cal.unselect();
      return;
  }

  // if we're still here, then show the modal
  show_booking_modal(cal, ds);
  return;
}

function show_booking_modal (cal, ds) {

  var vdate = moment(ds).format("DD-MM-YYYY");
  $("#newBookingModal").modal();
  $("#startDate").html(vdate);
  $("#start").val(vdate);
  cal.unselect();
}

function event_click (cal, info) {

  var dateStart = moment(info.event.start).format("DD-MMM-YYYY HH:mm");
  var dateEnd   = moment(info.event.end).format("DD-MMM-YYYY HH:mm");
  $("#bookingTitle").html(info.event.title);
  $("#bookingTitle").css({"background-color": info.el.style.backgroundColor});
  $("#bookingTitle").css({"color": info.el.style.color});
  $("#bookingType").html(info.event.extendedProps.eventType);
  $("#bookingInfo").html(info.event.extendedProps.description);
  $("#bookingStart").html(dateStart);
  if (dateEnd == 'Invalid date') {dateEnd=''};
  $("#bookingEnd").html(dateEnd);
  $("#checkBookingModal").modal();
  cal.unselect();

}
