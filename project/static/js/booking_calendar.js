
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
  eventLimit: false,
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

    // format clicked date to UTC string
    ds=moment.utc(info.dateStr);

    if (moment().diff(ds, 'days') > 0) {
      // if the date is in the past, then return and do no more...
      return;
    }

    var vdate = moment(ds).format("DD-MM-YYYY");
    var vurl = "/fpa/showdate/" + vdate;

    show_booking_modal(vurl);
    this.unselect();
  },
  select: function(arg) {
    // nothing...
  },
  eventClick: function(info) {
    event_click(this, info);
  },
  eventRender: function (info) {

    v_details = ""
    vurl = "/fpa/showttip/" + info.event.id + "/" + info.event.extendedProps.eventType;
    $.ajax({url: vurl, success: function(result) {
      $(info.el).tooltip({ title:result, html:true, animation:false, container:"body", boundary:'window' });
      }});


    // info.el.querySelector('.fc-title').innerHTML = info.event.title + " (" + info.event.extendedProps.availableSlots + ")";
    info.el.style = info.event.extendedProps.style;

  },
  dayRender: function (dayRenderInfo) {
      return dayRenderInfo.el
  }

}

function show_booking_modal (vurl) {

  $.ajax({url: vurl, success: function(result) {
    $("#model-content-opt").html(result);
  }});

  $("#newBookingModal").modal();
}

function event_click (cal, info) {

  ds=moment.utc(info.event.start.toISOString());
  var vdate = moment(ds).format("DD-MM-YYYY");
  var vevt  = info.event.extendedProps.eventType
  var vid   = info.event.id
  var vurl  = "/fpa/showevent/" + vdate + "/" + vevt + "/" + vid;
  show_booking_modal(vurl);
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
