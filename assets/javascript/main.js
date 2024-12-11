document.addEventListener('DOMContentLoaded', function() {
    const contributeLink = document.querySelector('a[href="./feed.html#post-box"]');
    const postBox = document.getElementById('post-box');

    // Function to add highlighting border around post-box
    function highlightPostBox() {
        if (postBox) {
            postBox.style.border = '2px solid #FFA500'; // Orange border
            setTimeout(() => {
                postBox.style.border = 'none'; // Remove border after 5 seconds
            }, 5000);
        }
    }

    // Function to handle clicking on contribute link
    function handleContributeLink(event) {
        event.preventDefault(); // Prevent default link behavior
        const hash = this.getAttribute('href'); // Get the hash value

        // Redirect to the specified URL
        window.location.href = hash;

        // Highlight the post-box
        highlightPostBox();
    }

    // Event listener for clicking on the contribute link
    if (contributeLink) {
        contributeLink.addEventListener('click', handleContributeLink);
    }

    // Check if the contribute link is not found or the user is not on the feed page
    if (!contributeLink || window.location.pathname !== '/feed.html') {
        // Highlight the post-box directly
        highlightPostBox();
    }
});



//toggle menu

const showSidebar = (toggleId, sidebarId, mainId) => {
    const toggle = document.getElementById(toggleId),
        sidebar = document.getElementById(sidebarId),
        main = document.getElementById(mainId)

    if (toggle && sidebar && main) {
        toggle.addEventListener('click', () => {
            /* open sidebar */
            sidebar.classList.toggle('show-sidebar');
            main.classList.toggle('main-pd');

            // Adjust main-container padding dynamically
            if (sidebar.classList.contains('show-sidebar')) {
                main.style.paddingLeft = sidebar.offsetWidth + 'px';
            } else {
                main.style.paddingLeft = '';
            }
        });
    }
}

showSidebar('navbar-top-toggle', 'sidebar', 'main');



function getTab(el) {
    const active = document.querySelector(".active");
    const visible = document.querySelector(".content-visible");
    const tabContent = document.getElementById(el.href.split("#")[1]);
  
    active.classList.toggle("active");
    visible.classList.toggle("content-visible");
  
    el.classList.add("active");
    tabContent.classList.add("content-visible");
  }
  
  document.addEventListener("click", (e) => {
    if (e.target.matches(".tab-item a")) {
      getTab(e.target);
    }
  });
  
  //contribute
  function setChooseForm(value) {
    const imageFields = document.getElementById('img-form');
    const codeFields = document.getElementById('text-form');
    // hide or show fields 
    if (value) {
        imageFields.style.display = 'block';
        codeFields.style.display = 'none';
    } else {
        imageFields.style.display = 'none';
        codeFields.style.display = 'block';
    }
}


function toggleForm(formToShow, formToHide) {
    document.getElementById(formToShow).style.display = "block";
    document.getElementById(formToHide).style.display = "none";
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button-post-box');
    buttons.forEach(button => button.classList.remove('active'));

    // Add active class to the clicked button
    document.querySelector(`button[data-form="${formToShow}"]`).classList.add('active');
}


var weatherModule = (function() {
	"use strict";
	var owm = {
		init: function() {
			this.cacheDom();
			this.bindEvents();
			this.callAPI();
		},
		cacheDom: function() {
			this.xBx = $("#xBxHack");
			this.user_input = $("#userCity");
			this.forcast = $("#forcast");
			this.city = $("#city");
			this.temp = $("#temperature");
			this.tempHigh = $("#high");
			this.tempLow = $("#low");
			this.set_icon = $("#set-icon").parent();
			this.weat_icon = $("#weather-icon");
			this.weat_icon_class = function(time_of_day) {
				var iconClass = "wi-owm-";

				if (time_of_day === "PM") {
					iconClass += "night-";
				} else {
					iconClass += "day-";
				}
				return iconClass;
			};
		},
		bindEvents: function() {
			this.city.click(this.events.checkBox.bind(this));
			this.city.hover(this.events.hover.bind(this));
			this.set_icon.click(this.events.checkBox.bind(this));
			this.user_input.keypress(this.events.enterKey.bind(this));
			this.user_input.blur(this.events.resetCheckBox.bind(this));
		},
		events: {
			checkBox: function(e) {
				e.preventDefault();
				this.xBx.prop("checked", true);
				this.user_input.focus();
			},
			resetCheckBox: function(e) {
				e.preventDefault();
				if (e.type === "keypress") {
					this.user_input.blur();
				}
				this.user_input.val("");
				this.xBx.prop("checked", false);
			},
			hover: function(e) {
				this.set_icon.toggleClass("hovered");
			},
			enterKey: function(e) {
				if (e.which === 13 || e.keyCode === 13) {
					e.preventDefault();
					this.callAPI(this.user_input.val());
					this.events.resetCheckBox.apply(this, [e]);
				}
			}
		},
		callAPI: function(url) {
			var apiUrl =
				"//api.openweathermap.org/data/2.5/weather?APPID=729f54a8e1485a86fe66063191eee57c&units=standard&q=";

			if (url === undefined || url === "") {
				url =
					"//api.openweathermap.org/data/2.5/weather?APPID=729f54a8e1485a86fe66063191eee57c&units=standard&q=dublin";
			} else {
				while (url.charAt(0) === " ") {
					url = url.substr(1);
				}
				apiUrl += encodeURIComponent(url);
				url = apiUrl.toLowerCase();
			}
			$.getJSON(url, this.parseData.bind(this));
		},
		parseData: function(json) {
			this.data = {
				name: json.name,
				weather: {
					description: json.weather[0].description,
					id: json.weather[0].id
				},
				temp: {
					current: Math.floor(json.main.temp),
					high: Math.floor(json.main.temp_max),
					low: Math.floor(json.main.temp_min)
				}
			};
			this.renderHTML();
		},
		renderHTML: function() {
			this.city.html(this.data.name);
			this.forcast.html(this.data.weather.description);
			this.temp.html(this.data.temp.current);
			this.tempHigh.html(this.data.temp.high);
			this.tempLow.html(this.data.temp.low);
			//DELETE CLASSES
			this.weat_icon.removeClass();
			//RESET CLASSES
			this.weat_icon.addClass("wi wi-fw weather-icon ");
			//ADD NEW CLASS
			this.weat_icon.addClass(this.weat_icon_class() + this.data.weather.id);
		}
	};
	owm.init();
	return {
		time_of_day: owm.weat_icon_class
	};
})();

/*

var timeModule = (function() {
	"use strict";
	var dateTime = {
		init: function() {
			this.cacheDom();
			this.render();
			this.refresh();
		},
		cacheDom: function() {
			this.date = new Date();
			this.time = $("#time");
			this.day = $("#day");
			this.month = $("#monDate");
		},
		refresh: function() {
			setInterval(function() {
				dateTime.date = new Date();
				dateTime.render();
			}, 1000);
		},
		render: function() {
			var currentMonth = [
					"Jan",
					"Feb",
					"Mar",
					"Apr",
					"May",
					"Jun",
					"Jul",
					"Aug",
					"Sep",
					"Oct",
					"Nov",
					"Dec"
				],
				currentDay = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
				month = this.date.getMonth(),
				date = this.date.getDate(),
				hour = this.date.getHours(),
				minutes = this.date.getMinutes(),
				day = this.date.getDay(),
				amPM;

			// CHECK TIME
						
			//IF MIDNIGHT
			if (hour === 0) {
				//HOUR EQUALS 12
				hour = 12;
			}
			//CHANGE 24 HOUR TO 12 HOUR
			if (hour > 12) {
				//MINUS 12
				hour -= 12;
				//CHANGE TO PM
				amPM = "PM";
			} else {
				//CHANGE TO AM
				amPM = "AM";
			}
			//IF HOUR IS LESS THAN 10
			if (hour < 10) {
				//ADD 0 TO HOUR
				hour = "0" + hour;
			}
			//GET MINUTES
			//IF MINUTES LESS THAN 10
			if (minutes < 10) {
				//ADD 0 TO MINUTES
				minutes = "0" + minutes;
			}
			//RENDER TIME
			this.time.html(hour + ":" + minutes + "<span>" + amPM + "</span>");
			//SET TIME OF DAT
			weatherModule.time_of_day(amPM);
			//RENDER DAY
			this.day.html(currentDay[day]);
			//RENDER DATE
			this.month.html(currentMonth[month] + " " + date);
		}
	};
	dateTime.init();
})();



const weekArray = ["Sun", "Mon", "Tue", "Wed", "Thr", "Fri", "Sat"];
const monthArray = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];
const current = new Date();
const todaysDate = current.getDate();
const currentYear = current.getFullYear();
const currentMonth = current.getMonth();

window.onload = function () {
  const currentDate = new Date();
  generateCalendarDays(currentDate);

  let calendarWeek = document.getElementsByClassName("calendar-week")[0];
  let calendarTodayButton = document.getElementsByClassName(
    "calendar-today-button"
  )[0];
  calendarTodayButton.textContent = `Today ${todaysDate}`;

  calendarTodayButton.addEventListener("click", () => {
    generateCalendarDays(currentDate);
  });

  weekArray.forEach((week) => {
    let li = document.createElement("li");
    li.textContent = week;
    li.classList.add("calendar-week-day");
    calendarWeek.appendChild(li);
  });

  const calendarMonths = document.getElementsByClassName("calendar-months")[0];
  const calendarYears = document.getElementsByClassName("calendar-years")[0];
  const monthYear = document.getElementsByClassName("calendar-month-year")[0];

  const selectedMonth = parseInt(monthYear.getAttribute("data-month") || 0);
  const selectedYear = parseInt(monthYear.getAttribute("data-year") || 0);

  monthArray.forEach((month, index) => {
    let option = document.createElement("option");
    option.textContent = month;
    option.value = index;
    option.selected = index === selectedMonth;
    calendarMonths.appendChild(option);
  });

  const currentYear = new Date().getFullYear();
  const startYear = currentYear - 60;
  const endYear = currentYear + 60;
  let newYear = startYear;
  while (newYear <= endYear) {
    let option = document.createElement("option");
    option.textContent = newYear;
    option.value = newYear;
    option.selected = newYear === selectedYear;
    calendarYears.appendChild(option);
    newYear++;
  }

  const leftArrow = document.getElementsByClassName("calendar-left-arrow")[0];

  leftArrow.addEventListener("click", () => {
    const monthYear = document.getElementsByClassName("calendar-month-year")[0];
    const month = parseInt(monthYear.getAttribute("data-month") || 0);
    const year = parseInt(monthYear.getAttribute("data-year") || 0);

    let newMonth = month === 0 ? 11 : month - 1;
    let newYear = month === 0 ? year - 1 : year;
    let newDate = new Date(newYear, newMonth, 1);
    generateCalendarDays(newDate);
  });

  const rightArrow = document.getElementsByClassName("calendar-right-arrow")[0];

  rightArrow.addEventListener("click", () => {
    const monthYear = document.getElementsByClassName("calendar-month-year")[0];
    const month = parseInt(monthYear.getAttribute("data-month") || 0);
    const year = parseInt(monthYear.getAttribute("data-year") || 0);
    let newMonth = month + 1;
    newMonth = newMonth === 12 ? 0 : newMonth;
    let newYear = newMonth === 0 ? year + 1 : year;
    let newDate = new Date(newYear, newMonth, 1);
    generateCalendarDays(newDate);
  });

  calendarMonths.addEventListener("change", function () {
    let newDate = new Date(calendarYears.value, calendarMonths.value, 1);
    generateCalendarDays(newDate);
  });

  calendarYears.addEventListener("change", function () {
    let newDate = new Date(calendarYears.value, calendarMonths.value, 1);
    generateCalendarDays(newDate);
  });
};

function generateCalendarDays(currentDate) {
  const newDate = new Date(currentDate);
  const year = newDate.getFullYear();
  const month = newDate.getMonth();
  const totalDaysInMonth = getTotalDaysInAMonth(year, month);
  const firstDayOfWeek = getFirstDayOfWeek(year, month);
  let calendarDays = document.getElementsByClassName("calendar-days")[0];

  removeAllChildren(calendarDays);

  let firstDay = 1;
  while (firstDay <= firstDayOfWeek) {
    let li = document.createElement("li");
    li.classList.add("calendar-day");
    calendarDays.appendChild(li);
    firstDay++;
  }

  let day = 1;
  while (day <= totalDaysInMonth) {
    let li = document.createElement("li");
    li.textContent = day;
    li.classList.add("calendar-day");
    if (todaysDate === day && currentMonth === month && currentYear === year) {
      li.classList.add("calendar-day-active");
    }
    calendarDays.appendChild(li);
    day++;
  }

  const monthYear = document.getElementsByClassName("calendar-month-year")[0];
  monthYear.setAttribute("data-month", month);
  monthYear.setAttribute("data-year", year);
  const calendarMonths = document.getElementsByClassName("calendar-months")[0];
  const calendarYears = document.getElementsByClassName("calendar-years")[0];
  calendarMonths.value = month;
  calendarYears.value = year;
}

function getTotalDaysInAMonth(year, month) {
  return new Date(year, month + 1, 0).getDate();
}

function getFirstDayOfWeek(year, month) {
  return new Date(year, month, 1).getDay();
}

function removeAllChildren(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}*/