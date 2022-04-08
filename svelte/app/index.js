import "./index.scss";
import $ from "jquery";
import "lazysizes";
import Modal from "modal-vanilla";
import Parallax from "parallax-js";
import SwiperCore, { Navigation, Pagination, Swiper } from "swiper/core";
import Selectise from "selectise";
// import Swiper styles
import "swiper/swiper-bundle.css";
import Inputmask from "inputmask";
import "lazysizes/plugins/parent-fit/ls.parent-fit";
import "./plugin/grt-youtube-popup";
// import datepicker from "js-datepicker";
import "regenerator-runtime/runtime.js";

import { Loader, LoaderOptions } from "google-maps";
import { correctPhoneWithMask } from "../src/helpers/correctPhoneWithMask";
import { sendTelegramMessage } from "../src/helpers/sendTelegramMessage";
import { captchaProtect } from "../src/helpers/grecaptcha";
import { phoneToNumbers } from "../src/helpers/phoneToNumbers";
import { setErrorInput } from "../src/helpers/setErrors";
import isEmail from "validator/es/lib/isEmail";
import {request} from "../src/api";

const options = {
  libraries: ['geometry', 'places']
};

const loader = new Loader("AIzaSyCMyW6HJLx8TXMlSemVjqMQkhb7-Bz8tGI", options);

SwiperCore.use([Navigation, Pagination]);

async function getCity(lat, lng) {
  console.info('getCity()');
  let cityStr = "";
  await loader.load();
  let latlng = new google.maps.LatLng(lat, lng);
  const geocoder = new google.maps.Geocoder();
  await geocoder.geocode({ latLng: latlng }, function (results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      console.log(results);
      if (results[1]) {
        for (let i = 0; i < results[0].address_components.length; i++) {
          for (
            let b = 0;
            b < results[0].address_components[i].types.length;
            b++
          ) {
            if (results[0].address_components[i].types[b] == "locality") {
              const city = results[0].address_components[i];
              cityStr = city.long_name;
              break;
            }
          }
        }
        // console.log({city})
      } /*else {
        alert("No results found");
      }*/
    } /*else {
      alert("Geocoder failed due to: " + status);
    }*/
  });
  console.log({ cityStr });
  return cityStr;
}

// const loader = new Loader("AIzaSyCMyW6HJLx8TXMlSemVjqMQkhb7-Bz8tGI", options);

// Swiper.use([Navigation, EffectCoverflow]);

// key=AIzaSyCMyW6HJLx8TXMlSemVjqMQkhb7-Bz8tGI
// global.jQuery = global.$ = $;
// let saveTop = 0;

const addressesFooter = document.querySelector(".bars");
const phoneHeaderLink = document.getElementById("phone_header");
const mobileHeaderPhoneLink = document.getElementById("mobile_header_phone");
let chosenCityNameInLocalStorage = localStorage.getItem("chosenCityName");
let cityHeader = document.getElementById("city_header");
const taxiLink = document.getElementById("orderTaxi");
const instagramLink = document.getElementById("inst");
const vkLink = document.getElementById("vk");
const yandexEdaLink = document.getElementById("yandex_eda_link");
console.log({ phoneHeaderLink, mobileHeaderPhoneLink });
let isCityInitialization = true;

const FEEDBACK_STATUSES = {
  send: 0,
  sent: 1,
}
let feedbackStatus = FEEDBACK_STATUSES.send;

async function getManagerSettings(){
  const response = await fetch('/manager_settings')
  window.managerSettings = (await response.json()).settings
  const managerSettingsGetEvent = new Event('managerSettingsGet')
  window.dispatchEvent(managerSettingsGetEvent)
}

getManagerSettings()

async function showTableStatus(restaurantMaps) {
  const urlSearchParams = new URLSearchParams(window.location.search)
  const filterDate = urlSearchParams.get('filter_date')
  const filterRestaurant = urlSearchParams.get('filter_restaraunt')
  if(!filterDate) return
  const tableNums = (await request('POST', '/reservation?type=check', {
    type: 'check',
    restaraunt: filterRestaurant,
    date:  filterDate.replace(/-/g, '/'),
    time: '16:00',
    phone: '-',
    persons: 0,
    table: 0,
    name: 'test',
    description: ''
  })).tables
  const tableIdsString = tableNums.map(num => `path[id='${num}']`).join(',')

  console.log({tableIdsString})
  restaurantMaps.forEach(map => [...map.querySelectorAll('path')].filter((path) => {
    if (!isNaN(path.id)) return path;
  }).forEach(path => {
    path.style.fill = 'green'
    path.classList.remove('reserved')
  }))
  if (tableIdsString) {
    restaurantMaps.forEach(map => {
      map.querySelectorAll(tableIdsString).forEach(path => {
        path.style.fill = 'red'
        path.classList.add('reserved')
      })
    })
  }

}

function appendSchemesAdmin(schemes) {
  // return
  // if (!document.getElementById("table")) return;
  const restaurantMaps = []
  document.querySelector("#table.admin").innerHTML = "";
  schemes.forEach((schema) => {
    let el = document.createElement("svg");
    console.log({SCHEMA_URL: schema.url});
    fetch(schema.url)
        .then((r) => r.text())
        .then((text) => {
          el.innerHTML = text;
          el.class = "svg";
          restaurantMaps.push(el)
          // document.querySelector("#table.admin").appendChild(el);
        })
        .then(() => showTableStatus(restaurantMaps))
        .then(() => {
          document.querySelector("#table.admin").append(...restaurantMaps);
        })
        .catch(console.error.bind(console));
  });

}

async function initCity() {
  function setCurrentCity(currentCity) {
    window.currentCity = currentCity;
    const cityChangedEvent = new Event("currentCityChange");
    window.dispatchEvent(cityChangedEvent);
    if (!isCityInitialization) {
      window.location.href = `/set_city_id?id=${currentCity.id}`;
    }
    isCityInitialization = false;
    const adminTableWrapper = document.querySelector('#table.admin')
    if(adminTableWrapper){
      const selectAdminRestaraunts = document.querySelector('select[name="filter_restaraunt"]').options
      const selectedRestarauntId = selectAdminRestaraunts.item(selectAdminRestaraunts.selectedIndex);
      let restaurantsInCity = null;
      if(selectedRestarauntId.value)
        restaurantsInCity = window.restaraunts.filter(r => r.id == selectedRestarauntId.value)
      else
        restaurantsInCity = window.restaraunts.filter(r => r.city.name === currentCity.name)
      if(restaurantsInCity){
// console.log({restaurantsInCity})
        appendSchemesAdmin(restaurantsInCity[0].schemes)
      }
    }
    // fetch(`/set_city_id?id=${currentCity.id}`).then(() => document.location.reload())
  }

  function setCurrentCityData(currentCity) {
    addressesFooter.innerHTML = currentCity.addresses
      .map((r, i) => `<li>${r.address}${currentCity.addresses.length - 1 !== i ? ',' : ''}</li>`)
      .join("");
    // console.log({addresses: currentCity.addresses.map(c => c.address).join(',<br>')})
    // cityHeader.value = currentCity.name;
    // console.log({cityHeader})
    // const cityOptions = cityHeader.querySelector('.selectise-options');
    // const chosenCity = [...cityOptions.children].find(el => el.dataset.value === currentCity.name)
    // const cityOptionsWithoutChosenCity = [...cityOptions.children].filter(el => el.dataset.value !== currentCity.name)
    // console.log({chosenCity})
    // const sortedCityOptions = [chosenCity, ...cityOptionsWithoutChosenCity];
    // cityOptions.innerHTML = ''
    // cityOptions.append(...sortedCityOptions)
    document.querySelector(".selectise-trigger").textContent = currentCity.name;
    if (currentCity.phone) {
      phoneHeaderLink.href = mobileHeaderPhoneLink.href =
        "tel:" + phoneToNumbers(currentCity.phone);
      phoneHeaderLink.querySelector("span").textContent = currentCity.phone;
    }
    if (currentCity.instagram) instagramLink.href = currentCity.instagram;
    if (currentCity.vk) vkLink.href = currentCity.vk;
    console.log({ currentCity });
    //Только первый адрес сейчас обрабатывается
    if (currentCity.addresses && currentCity.addresses[0]?.coordinates) {
      const [lat, lng] = currentCity.addresses[0].coordinates
        .split(",")
        .map((el) => el.trim());
      taxiLink.href = `https://3.redirect.appmetrica.yandex.com/route?end-lat=${lat}&end-lon=${lng}&appmetrica_tracking_id=1178268795219780156`;
      initMap(+lat, +lng);
    }

    if (currentCity.addresses.find((r) => r.yandex_eda)) {
      yandexEdaLink.target = "_blank";
      yandexEdaLink.href = currentCity.addresses.find(
        (r) => r.yandex_eda
      ).yandex_eda;
    } else {
      yandexEdaLink.target = "_self";
      yandexEdaLink.href = "#";
    }
  }

  function renderCity() {
    const cityInLocalStorage = window.cities.find(
      (city) => city.name === chosenCityNameInLocalStorage
    );
    if (cityInLocalStorage) {
      setCurrentCity(cityInLocalStorage);
      setCurrentCityData(cityInLocalStorage);
    } else {
      if (window.cities.length > 0) {
        localStorage.setItem("chosenCityName", window.cities[0].name);
        setCurrentCity(window.cities[0]);
        setCurrentCityData(window.cities[0]);
      }
    }
  }

  if (!chosenCityNameInLocalStorage) {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;
          const userCity = await getCity(lat, lng);
          console.log({ userCity });
          let currentCity;
          if (!userCity) currentCity = cities[0];
          else
            currentCity =
              cities.find(
                (city) =>
                  city.name.includes(userCity) || userCity.includes(city.name)
              ) || cities[0];

          setCurrentCity(currentCity);
          console.log({ currentCity });
          // if(!currentCity) return
          chosenCityNameInLocalStorage = currentCity.name;
          localStorage.setItem("chosenCityName", currentCity.name);
          console.log("first");
          renderCity();
        },
        (error) => {
          console.log(error);
          if (!localStorage.getItem("chosenCityName")) {
            setCurrentCity(cities[0]);
            setCurrentCityData(cities[0]);
            localStorage.setItem("chosenCityName", cities[0].name);
          }
        }
      );
    }
  }
  // console.log('second')
  if (chosenCityNameInLocalStorage) {
    renderCity();
  }

  cityHeader.addEventListener("change", (e) => {
    console.log("city changed!!");
    if (e.target.value === "") {
      localStorage.removeItem("chosenCityName");
      addressesFooter.innerHTML = "";
      phoneHeaderLink.href = mobileHeaderPhoneLink.href = "tel:88004440155";
      phoneHeaderLink.querySelector("span").textContent = "8 (800) 444-01-55";
      return;
    }
    const currentCity = cities.find((el) => el.name === e.target.value);
    setCurrentCity(currentCity);
    setCurrentCityData(currentCity);
    // const currentCityAddresses = currentCity.addresses.map(r => r.address);

    localStorage.setItem("chosenCityName", currentCity.name);
    // addresses_header.innerHTML = currentCityAddresses.join("<br>");
    //
    // if(currentCity.phone){
    //   phoneHeaderLink.href = phoneFooterLink.href = mobileHeaderPhoneLink.href =
    //       "tel:" + phoneToNumbers(currentCity.phone);
    //   phoneFooterLink.textContent = phoneHeaderLink.querySelector(
    //       "span"
    //   ).textContent = currentCity.phone;
    // }
    // instagramLink.href = currentCity.instagram
    // vkLink.href = currentCity.vk
    //
    // taxiLink.href=`https://3.redirect.appmetrica.yandex.com/route?end-lat=${currentCity.lat}&end-lon=${currentCity.lng}&appmetrica_tracking_id=1178268795219780156`
  });
}

//TODO update city logic
window.restaraunts = [];
fetch("/restaraunts", { method: "GET" })
  .then((data) => data.json())
  .then((body) => {
    window.restaraunts = body;
    window.cities = [];
    window.restaraunts.forEach((r) => {
      console.log({ r });
      if (!cities.find((el) => el.name === r.city.name)) {
        cities.push({
          id: r.city.id,
          name: r.city.name,
          instagram: r.city.instagram,
          vk: r.city.vk,
          phone: r.city.phone,
          city_timezone: r.city.city_timezone,
          addresses: window.restaraunts.filter(
            (rest) => rest.city.name === r.city.name
          ),
        });
      }
    });
    window.cities = cities;
    for (const city of cities) {
      const cityOption = document.createElement("option");
      cityOption.value = cityOption.textContent = city.name;
      cityOption.classList.add("option", "selectise-option");
      cityHeader.append(cityOption);
    }
    const selectiseCityHeader = new Selectise(cityHeader, {
      onSelect(e) {
        const event = new Event("change");
        // event.target = {}
        console.log({ e, event });
        cityHeader.value = e.selectionValue;
        cityHeader.dispatchEvent(event);
      },
    });
    cityHeader = document.getElementById("city_header");
    initCity();
  });
// key=AIzaSyCMyW6HJLx8TXMlSemVjqMQkhb7-Bz8tGI
global.jQuery = global.$ = $;
let saveTop = 0;

function openModal(id) {
  $(".modal").removeClass("show").hide();
  saveTop = $("html").scrollTop();
  // $(".modal-title").text(title);
  // $(".modal-subtitle").text(subtitle);
  $("html,body").addClass("locked");
  $("body").css("overflow", "hidden");
  $("body").css("top", -saveTop);
  $(id).addClass("show").show();
}

function detectmob() {
  if (
    navigator.userAgent.match(/Android/i) ||
    navigator.userAgent.match(/webOS/i) ||
    navigator.userAgent.match(/iPhone/i) ||
    navigator.userAgent.match(/iPad/i) ||
    navigator.userAgent.match(/iPod/i) ||
    navigator.userAgent.match(/BlackBerry/i) ||
    navigator.userAgent.match(/Windows Phone/i)
  ) {
    return true;
  } else {
    return false;
  }
}

$(".call,.open-modal").on("click", function (e) {
  e.preventDefault();
  var myModal = new Modal({
    el: document.getElementById("static-modal"),
  }).show();
});

// $("#jobmodal-btn").on("click", openJobModal);
// $(".clickme").on("click", openJobModal);
$(".login.sign.gradient1").on("click", function (e) {
  e.preventDefault();
  openModal("#signinup");
});
if ($("html").scrollTop() > $(".navbar").height()) $("body").addClass("fixed");
else $("body").removeClass("fixed");

function number(value) {
  return parseFloat(value)
    .toFixed()
    .replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ");
}

function setCookie(name, value, props) {
  props = props || {};
  var exp = props.expires;

  if (typeof exp == "number" && exp) {
    var d = new Date();
    d.setTime(d.getTime() + exp * 1000);
    exp = props.expires = d;
  }

  if (exp && exp.toUTCString) {
    props.expires = exp.toUTCString();
  }
  value = encodeURIComponent(value);
  var updatedCookie = name + "=" + value;
  for (var propName in props) {
    updatedCookie += "; " + propName;
    var propValue = props[propName];
    if (propValue !== true) {
      updatedCookie += "=" + propValue;
    }
  }
  document.cookie = updatedCookie;
}

function submitJobForm() {
  // Отправка формы по вакансии

  /// Успешный исход
  console.log(213);
  openModal("#succesjob");
  return true;
}

var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");

  if (x.length === 0) return false;
  x[n].style.display = "flex";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == x.length - 1) {
    document.getElementById("nextBtn").innerHTML = "Отправить";
  } else {
    document.getElementById("nextBtn").innerHTML = "Далее";
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n);
}

function nextPrev(n, shouldValidate = true) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (shouldValidate) {
    if (n == 1 && !validateForm()) return false;
  }
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  console.log(`current tab is ${currentTab} and (currentTab >= x.length):`)
  console.log(currentTab >= x.length)

  if (currentTab >= x.length) {
    //...the form gets submitted:
    currentTab = 0;
    // submitJobForm();
    // return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x,
    y,
    i,
    valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i,
    x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}

//   const events = new Swiper(".col-container", {
//         slidesPerView: 5,
//           loop: true,
//           navigation: {
//     nextEl: '.next-event',
//     prevEl: '.prev-event',
//   },
//         spaceBetween: 0,

//       });
const swiper = new Swiper(".swiper-container", {
  // Optional parameters
  loop: true,
  spaceBetween: 15,
  // Navigation arrows
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

async function initMap(lat = 54.964361, lng = 82.93014) {
  await loader.load();
  console.info("initMap()");
  var center = new google.maps.LatLng(lat, lng);

  if (detectmob()) {
    center = new google.maps.LatLng(lat, lng);
  }
  var factory = new google.maps.LatLng(lat, lng);
  var mapOptions = {
    center: center,
    zoom: 16,
    scrollwheel: !1,
    navigationControl: !1,
    mapTypeControl: !1,
    scaleControl: !1,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  };
  var map = new google.maps.Map(
      document.getElementById("map-canvas"),
      mapOptions
  );
  window.map = map;
  var content =
      '<div id="iw-container">' +
      '<div class="iw-title">ооо «СТМ-КОСМЕТИКА»</div>' +
      '<div class="iw-content">' +
      '<div class="iw-subTitle">г. Новосибирск,<br/>проспект Мира, 62</div>' +
      '<p>+7 (383) 249-7929<br/>+7 962 829 7929<br/><a href="mailto:anton@stm-cosmetics.ru">anton@stm-cosmetics.ru</a></p>' +
      "</div>";

  function CustomMarker(latlng, map, args) {
    this.latlng = latlng;
    this.args = args;
    this.setMap(map);
  }

  CustomMarker.prototype = new google.maps.OverlayView();
  CustomMarker.prototype.draw = function () {
    var self = this;
    var div = this.div;
    if (!div) {
      div = this.div = document.createElement("div");
      // div.innerHTML =
      //     '<div class="iw-title">ооо «СТМ-КОСМЕТИКА»</div>' +
      //     '<div class="iw-content">' +
      //     '<div class="iw-subTitle">г. Новосибирск,<br/>проспект Мира, 62</div>' +
      //     '<p style="margin-top:4px;"><a href="tel:+7(383)247-7929">+7 (383) 247-7929</a><a href="mailto:anton@stm-cosmetics.ru">anton@stm-cosmetics.ru</a></p>';
      div.className = "marker";
      div.style.position = "absolute";
      div.style.cursor = "pointer";
      div.style.width = "340px";
      div.style.height = "206px";
      div.style.color = "white";
      div.style.background =
          "url(" + require("./images/mapback.png") + ") no-repeat top left";
      div.style["background-size"] = "contain";
      if (typeof self.args.marker_id !== "undefined") {
        div.dataset.marker_id = self.args.marker_id;
      }
      google.maps.event.addDomListener(div, "click", function (event) {
        google.maps.event.trigger(self, "click");
      });
      var panes = this.getPanes();
      panes.overlayImage.appendChild(div);
    }
    var point = this.getProjection().fromLatLngToDivPixel(this.latlng);
    if (point) {
      div.style.left = point.x - 305 + "px";
      div.style.top = point.y - 185 + "px";
    }
  };
  CustomMarker.prototype.remove = function () {
    if (this.div) {
      this.div.parentNode.removeChild(this.div);
      this.div = null;
    }
  };
  CustomMarker.prototype.getPosition = function () {
    return this.latlng;
  };
  var overlay = new CustomMarker(factory, map, {
    marker_id: "123",
    colour: "Red",
  });
}

console.log({ req: require("./images/ajax_loader_blue_64.gif") });

function sbm(th) {
  var formData = {
    // 'title'             : $(th).find('input[name=subject]').val(),
    name: $(th).find("input[name=name]").val(),
    // 'city'             : $(th).find('input[name=city]').val(),
    // 'email'             : $(th).find('input[name=email]').val(),
    phone: $(th).find("input[name=phone]").val(),
    // 'description'    : $(th).find('textarea').val()
  };
  $(th).find("input[type=submit]").replaceWith(`<img 
        style="width: 42px !important;height: 42px !important;margin: 5px 100px;"
        src="${require("./images/ajax_loader_blue_64.gif")}" />`);

  $.ajax({
    type: "POST", // define the type of HTTP verb we want to use (POST for our form)
    url: "https://fr.respublica.bar/mail.php", // the url where we want to POST
    data: formData, // our data object
    dataType: "json", // what type of data do we expect back from the server
    encode: true,
  })
    .done(function (data) {
      if (data.result === "ok") {
        ym(55962916, "reachGoal", "lead");
        gtag("event", "zayavka", {
          event_category: "zayavka",
          event_action: "zayavka",
        });
        $(th).html('<div class="success">Спасибо, мы с вами свяжемся!</div>');
      } else $(th).html('<div class="success">Произошла ошибка!</div>');
    })
    .catch((err) => {
      console.error(err);
    });
  return false;
}

function nextStage(th) {
  if ($(th).next().hasClass("stage")) {
    $(th).hide();
    $(th).next().show();
  }
}

$(function () {
  // const picker = datepicker(".datepicker", {
  //   customDays: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
  //   formatter: (input, date, instance) => {
  //     const value = date.toLocaleDateString();
  //     input.value = value.replaceAll("/", "."); // => '1/1/2099'
  //   },
  //   overlayPlaceholder: "Год в формате гггг",
  //   customMonths: [
  //     "Январь",
  //     "Февраль",
  //     "Март",
  //     "Апрель",
  //     "Май",
  //     "Июнь",
  //     "Июль",
  //     "Август",
  //     "Сентябрь",
  //     "Октябрь",
  //     "Ноябрь",
  //     "Декабрь",
  //   ],
  //
  //   onSelect: (instance, date) => {
  //     // Do stuff when a date is selected (or unselected) on the calendar.
  //     // You have access to the datepicker instance for convenience.
  //   },
  // });
  function switchMainBanner(slideSelector) {
    if (window.matchMedia('(min-width: 768px)').matches) {
      let mainBannerImg = window.managerSettings.main_banner;
      if (mainBannerImg) {
        slideSelector
        .css('background-image', 'url(/media/' + mainBannerImg + ')');
      }
    } else {
      let mainBannerImg = window.managerSettings.main_banner_mobile;
      if (mainBannerImg) {
        slideSelector
        .css('background-image', 'url(/media/' + mainBannerImg + ')');
      }
    }
  }

  $(window).on('managerSettingsGet', () => {
    let paymentRulesContent = window.managerSettings.payment_and_return;
    console.log({paymentRulesContent});
    $("#paymentRulesModal").find('.modal-description').html(paymentRulesContent);
    const slideSelector = $("#main-page");
    if (slideSelector) {
      switchMainBanner(slideSelector);
      $(window).on('resize', () => {
        switchMainBanner(slideSelector);
      });
    }
  });

  $("input[type='number']").on("keydown", function () {
    // Save old value.
    if (
      !$(this).val() ||
      (parseInt($(this).val()) <= 11 && parseInt($(this).val()) >= 0)
    )
      $(this).data("old", $(this).val());
  });
  $("input[type='number']").on("keyup", function () {
    // Check correct, else revert back to old value.
    if (
      !$(this).val() ||
      (parseInt($(this).val()) <= 11 && parseInt($(this).val()) >= 0)
    );
    else $(this).val($(this).data("old"));
  });
  $(".code-input").on("keyup", function () {
    console.log({ val: $(this).val() });
    if ($(this).next().hasClass("code-input") && $(this).val() !== "")
      $(this).next().trigger("focus");
  });
  $(".verify-registration").on("click", function () {
    const code =
      $("#register input[name='code1']").val().toString() +
      $("#register input[name='code2']").val().toString() +
      $("#register input[name='code3']").val().toString() +
      $("#register input[name='code4']").val().toString();
    console.log(code);
    // Проверка кода для регистрации и вход по сессии
  });
  $(".reset-password").on("click", function () {
    const code =
      $("#forgot-password input[name='code1']").val().toString() +
      $("#forgot-password input[name='code2']").val().toString() +
      $("#forgot-password input[name='code3']").val().toString() +
      $("#forgot-password input[name='code4']").val().toString();
    console.log(code);
  });

  function setErrorShadow(el) {
    el.classList.add("error-shadow");
    setTimeout(() => {
      el.classList.remove("error-shadow");
    }, 3000);
  }

  $(".checkout-final").on("click", function (e) {
    const currentStage = e.target.closest(".stage");
    const nameInputEl = currentStage.querySelector('input[name="name"]');
    const addressInputEl = currentStage.querySelector('input[name="addres"]');
    const phoneInputEl = currentStage.querySelector('input[name="phone"]');
    if (currentStage) {
      if (
        nameInputEl.value.trim() === "" ||
        addressInputEl.value.trim() === "" ||
        phoneInputEl.value.trim() === "" ||
        phoneInputEl.value.trim().includes("_")
      ) {
        if (nameInputEl.value.trim() === "") setErrorShadow(nameInputEl);
        if (addressInputEl.value.trim() === "") setErrorShadow(addressInputEl);
        if (
          phoneInputEl.value.trim() === "" ||
          phoneInputEl.value.trim().includes("_")
        )
          setErrorShadow(phoneInputEl);

        return;
      }
    }
    captchaProtect(() => {
      // обработка заказа
      const checkoutData = $("#checkoutform").serializeArray();

      // Успешный исход

      const cartItemsTitlesWithQuantity = [
        ...document.querySelector(".cart-full").querySelectorAll(".cart-item"),
      ].map(
        (el) =>
          `${el.querySelector(".cart-item_title").textContent} * ${
            el.querySelector(".item-quantity").textContent
          }`
      );
      sendTelegramMessage(
        `${nameInputEl.value.trim()} заказал доставку на адрес "${addressInputEl.value.trim()}". Блюда: ${cartItemsTitlesWithQuantity.join(
          ", "
        )}. Номер: ${phoneInputEl.value.trim()}. Цена заказа: ${
          document.querySelector(".cart-summary").textContent
        }.`
      );
      nextStage($(this).parents(".stage"));
    });
  });

  const personalForm = document.querySelector(".edit-personal");
  if (personalForm) {
    const [
      lastNameInput,
      firstNameInput,
      secondNameInput,
      birthdayInput,
      emailInput,
      passwordInput,
    ] = personalForm.querySelectorAll("input");
    // const startData = {fio: fioInput.value, phone: phoneInput.value}
    birthdayInput.onchange = (e) => {
      console.log(e.target.value.length);
      if (e.target.value.length === 11) {
        console.log(e.target.value);
        e.target.value = e.target.value.slice(1);
      }
    };
    $("#update-personal").on("click", function (e) {
      e.preventDefault();
      console.log({
        // fioInput,
        lastNameInput: lastNameInput.value,
        firstNameInput: firstNameInput.value,
        secondNameInput: secondNameInput.value,
        // phoneInput: phoneInput.value,
        birthdayInput: birthdayInput.value,
        isEmail: isEmail(emailInput.value.trim()),
        passwordInput,
      });
      console.log({ val: lastNameInput.value.trim() });

      let inputErrors = false;

      const lastNameValue = lastNameInput.value.trim();
      const firstNameValue = firstNameInput.value.trim();
      const secondNameValue = secondNameInput.value.trim();
      const emailValue = emailInput.value.trim();
      const birthdayValue = birthdayInput.value.trim();

      if (!lastNameValue) {
        setErrorInput(lastNameInput);
        inputErrors = true;
      }
      if (!firstNameValue) {
        setErrorInput(firstNameInput);
        inputErrors = true;
      }
      if (!secondNameValue) {
        setErrorInput(secondNameInput);
        inputErrors = true;
      }
      if (!!emailValue && !isEmail(emailValue)) {
        setErrorInput(emailInput);
        inputErrors = true;
      }
      if (
          !!birthdayValue &&
          +birthdayInput.value.slice(0, 4) < 1920
      ) {
        setErrorInput(birthdayInput);
        inputErrors = true;
      }

      const minPasswordLength = 6;
      const passwordValue = passwordInput.value.trim();
      let passwordErrors = [];

      // Check if there are at least minPasswordLength latin or numeric simbols
      const passwordRE = new RegExp(`[0-9a-zA-Z]{${minPasswordLength},}`);
      if (!passwordRE.test(passwordValue)) {
          passwordErrors.push('password is too short');
      }
      
      // Check if there are non latin simbols and special simbols: 
      const passwordRE2 = new RegExp(`[^0-9a-zA-Z]`); 
      if (passwordRE2.test(passwordValue)) {
          passwordErrors.push('password has non latin simbols that isn\'t arabic figures');
      }

      if (!!passwordErrors.length) {
          openModal('#personal-update-errors');
          const modalEl = $('#personal-update-errors');
          let modalTextEl = modalEl.find('.modal-content');
          modalTextEl.text('Пароль должен быть не менее 6 символов длинной и состоять из латинских букв и цифр.');
          return;
      }

      if (inputErrors) {
        return;
      }

      fetch("/personal", {
        method: "POST",
        body: JSON.stringify({
          fio: `${lastNameValue} ${firstNameValue} ${secondNameValue}`,
          email: emailValue,
          birthday: birthdayValue,
          password: passwordValue,
        }),
      }).then(() => (window.location.href = "/personal"));
      console.log("clicked");
    });
  }

  $(".checkout-btn").on("click", function (e) {
    if ($(this).hasClass('disabled')) return;
    const cartSummaryEl = document.querySelector(".cart-summary");
    console.log({ cartSummaryEl });

    if (cartSummaryEl) {
      if (+cartSummaryEl.textContent.slice(0, -1) < 500) {
        setErrorShadow(document.querySelector('.cart-sum .cart-summary_amount'))
        return;
      }
    }
    const cartInDom = document.querySelector(".cart-full.pb-sm-4.mb-4");
    if (cartInDom.children.length === 0) return;
    nextStage($(this).parents(".stage"));
  });
  $(".send-reset").on("click", function () {
    // Отправка СМС при регистрации
    const phone = $("#forgot-password .phone-input").val();
    // Успешный исход
    nextStage($(this).parents(".stage"));
  });
  $(".send-register").on("click", function () {
    // Отправка СМС при регистрации
    const phone = $("#register .phone-input").val();
    // Успешный исход
    nextStage($(this).parents(".stage"));
  });
  let jobFormLevel = 0;

  $("#nextBtn").on("click", function (e) {
    e.preventDefault();
    console.log({ jobFormLevel });
    const regForm = document?.getElementById("regForm");
    // const whereWantToWork = document?.getElementById("whereWantToWork");
    const jobModal = e.target.closest("#jobmodal");
    const isJobModal = !!jobModal;
    if (jobFormLevel === 0) {
      if (isJobModal) {
        const phoneInput = jobModal.querySelector(".phone-input");
        const firstName = jobModal.querySelector(".first_name");
        const lastName = jobModal.querySelector(".last_name");
        const middleName = jobModal.querySelector(".middle_name");
        if (
          !correctPhoneWithMask(phoneInput.value) ||
          !firstName.value.trim() ||
          !lastName.value.trim()
        ) {
          if (!firstName.value.trim()) {
            setErrorShadow(firstName);
          }
          if (!lastName.value.trim()) {
            setErrorShadow(lastName);
          }
          // if (!middleName.value.trim()) {
          //   setErrorShadow(middleName);
          // }
          if (!correctPhoneWithMask(phoneInput.value)) {
            setErrorShadow(phoneInput);
          }
          return;
        }

        if (
          e.target.textContent === "Отправить" ||
          !regForm?.querySelector("#rules").checked
        )
          return;
        jobFormLevel = 1;
        nextPrev(1, false);
        return;
      }
    }
    let selectsValues = [];
    const workSelects = [
      ...document.querySelectorAll("#whereWantToWork select"),
    ];
    console.log({ workSelects });

    if (workSelects.length > 0) {
      workSelects.forEach((select) => {
        selectsValues.push(...select.selectedOptions);
      });
      selectsValues = selectsValues.map((val) =>
        val.textContent.startsWith("Выбери")
      );
      console.log({ selectsValues });
    }
    console.log("level", jobFormLevel === 1);
    if (jobFormLevel === 1) {
      const jobSelect = jobModal.querySelector("[name=job]");
      const citySelect = jobModal.querySelector("[name=city]");
      if (!jobSelect.value || !citySelect.value) return;
      jobFormLevel = 2;
      // console.log({jobFormLevel})

      nextPrev(1, false);
      return;
    }
    // if(jobFormLevel === 2) {
    //   console.log('test')
    // }
    // if (
    //   e.target.textContent === "Отправить" ||
    //   !regForm?.querySelector("#rules").checked
    // )
    //   return;
    nextPrev(1, false);
  });
  $("#prevBtn").on("click", function () {
    jobFormLevel--;
    nextPrev(-1);
  });
  $(".reserve").on("click", function (e) {
    e.preventDefault();
    // Бронирование

    //Успешный исход
    openModal("#reserved");
    // Подстановка кода
    $("#reserved .modal-subtitle").text("282313");
  });
  $(".select-table").on("click", function (e) {
    e.preventDefault();
    // Выбор стола
  });
  $(".send-feedback").on("click", function (e) {
    e.preventDefault();
    // Отправка отзыва

    // Успешный исход
    $('#feedback input').each((i, el)=>{el.value=""});
    $('#feedback textarea').each((i, el)=>{el.value=""});
    $(
      "#feedback .modal-title,#feedback a,#feedback input,#feedback textarea,#feedback .modal-description"
    ).hide();
    $("#feedback .success").show();
    feedbackStatus = FEEDBACK_STATUSES.sent;
  });
  $(".only-menu .dish-item").on("click", function () {
    openModal("#item");
  });

  function setModalData(modal, dishItem) {
    modal.dataset.id = dishItem.id;
    modal.querySelector(".dish-img").src =
      dishItem.querySelector(".dish-img").src;
    modal.querySelector(".dish-description").textContent =
      dishItem.querySelector(".dish-description").textContent;
    modal.querySelector(".dish-details_price").textContent =
      dishItem.querySelector(".dish-details_price").textContent;
    modal.querySelector(".modal-title").textContent =
      dishItem.querySelector(".dish-title").textContent;

    modal.querySelector(".dish-details_sizes").textContent =
      dishItem.querySelector(".dish-details_sizes").textContent + " /";
    if (!dishItem.querySelector(".item-quantity")) {
      if (modal.querySelector(".calculations"))
        modal.querySelector(".calculations").outerHTML = "";
      return;
    }
    modal.querySelector(".item-quantity").textContent =
      dishItem.querySelector(".item-quantity").textContent;
  }

  $(".dish-item").on("click", function (e) {
    const modal = document.getElementById("item-buy");
    const dishItem = e.target.closest(".dish-item");
    setModalData(modal, dishItem);
    openModal("#item-buy");
  });
  $(".delete-account").on("click", function (e) {
    e.preventDefault();
    // Удаление аккаунта
    request('POST', '/deactivate')
      .then(() => {
        // Успешный исход
        $("#deleteaccount .modal-title,#deleteaccount a").hide();
        $("#deleteaccount .success").show();
        window.location.href = '/';
      });
  });

  $(".exit-account").on("click", function (e) {
    e.preventDefault();
    request('POST', '/exit')        
      .then(() => {
      $("#exitaccount .modal-title,#exitaccount a").hide();
      $("#exitaccount .success").show();
      window.location.href = '/';
    })
  });

  
  $(".big-offer .close").on("click", function (e) {
    e.preventDefault();
    $(".big-offer").addClass("hide");
  });
  if (document.querySelector("#scene")) {
    var scene = document.getElementById("scene");
    var parallaxInstance = new Parallax(scene);
  }
  $("form").on("submit", function (event) {
    sbm(this);
    return false;
  });
  //     loader.load().then(function (google) {
  //         initMap();
  // });
  var selector = [
    ...document.querySelectorAll(".phone-input"),
    ...document.querySelectorAll("input[name=phone]"),
  ];
  var im = new Inputmask("+7(999)-999-99-99");
  selector.forEach((node) => {
    im.mask(node);
  });

  $(".view").on("click", function () {
    $(".modal-box").hide();
    saveTop = $("html").scrollTop();
    $(".modal-wrapper").fadeIn(400);
    $("html,body").addClass("locked");
    $("body").css("overflow", "hidden");
    $("body").css("top", -saveTop);
    $("#video").show();
    $("#video iframe").attr("src", $("#video iframe").attr("data-src"));
  });

  const state = [
    { value: "98 000", title: 'Формат "Опция"' },
    { value: "157 000", title: 'Формат "Эконом"' },
    { value: "221 000", title: 'Формат "Лайт"' },
    { value: "352 000", title: 'Формат "Стандарт"' },
    { value: "629 000", title: 'Формат "Премиум"' },
  ];

  function t(t) {
    $(t).on("click", function (t) {
      t.preventDefault();
      $(this).parent().fadeOut();
    });
  }

  $(".dropdown-toggle").on("click", function () {
    var t = $(this)
      .parents(".button-dropdown")
      .children(".dropdown-menu")
      .is(":hidden");
    $(".button-dropdown .dropdown-menu").hide();
    $(".button-dropdown .dropdown-toggle").removeClass("active");
    if (t) {
      $(this)
        .parents(".button-dropdown")
        .children(".dropdown-menu")
        .toggle()
        .parents(".button-dropdown")
        .children(".dropdown-toggle")
        .addClass("active");
    }
  });
  $(document).on("click", function (t) {
    var n = $(t.target);
    if (!n.hasClass("dropdown-toggle")) {
      $(".button-dropdown .dropdown-menu").hide();
      $(".button-dropdown .dropdown-toggle").removeClass("active");
    }
  });
  $("[data-modal]").on("click", function (e) {
    console.log("clicked");
    e.preventDefault();
    openModal($(this).attr("href") || $(this).attr("data-modal"));
    if ($(this).attr('href') === '#career-video') {
      document.querySelector('#career-video video').play()
    }
  });
  $("#get-policy").on("click", function () {
    openModal(
      "#policy",
      "Политика в отношении обработки персональных данных",
      ""
    );
  });
  // initRangeEl();

  $(".navbar-toggler").on("click", function () {
    $("#menu").fadeToggle(300);
    $(this).toggleClass("activated");
    $("html,body").toggleClass("locked");
  });
  $(".modal-wrapper").on("click", function (e) {
    e.stopPropagation();
    $("#video iframe").attr("src", "");
    const targ = $(e.target);
    if (targ.hasClass("modal-wrapper")) {
      $(".modal-wrapper").fadeOut(400);
      $("html,body").removeClass("locked");
      $("body").css("overflow", "auto");
      $("html").scrollTop(saveTop);
      if (targ.attr('id') === "feedback" && feedbackStatus === FEEDBACK_STATUSES.sent) {
        $(
          "#feedback .modal-title,#feedback a,#feedback input,#feedback textarea,#feedback .modal-description"
        ).show();
        $("#feedback .success").hide();
        feedbackStatus = FEEDBACK_STATUSES.send;
      }
      if (targ.attr('id') === 'career-video') {
        document.querySelector('#career-video video').pause()
      }
    }

  });

  $("#paymentRules").on("click", function (e) {
    openModal("#paymentRulesModal");
  });
  $("#visit_rules").on("click", function (e) {
    openModal("#visitRulesModal");
  });

  $(window).on("scroll", function () {
    if ($("html").scrollTop() > $(".navbar").height())
      $("body").addClass("fixed");
    else $("body").removeClass("fixed");
  });
  $(".btn-color").on("click", function () {
    openModal("#mainform", $(this).data("title"), $(this).data("subtitle"));
  });
  $(".modal-wrapper .close,.close-modal").on("click", function (e) {
    e.preventDefault();
    $(".modal-wrapper").fadeOut(400).removeClass("show");
    $("html,body").removeClass("locked");
    $("body").css("overflow", "auto");
    $("html").scrollTop(saveTop);

    if (feedbackStatus === FEEDBACK_STATUSES.sent) {
      $(
        "#feedback .modal-title,#feedback a,#feedback input,#feedback textarea,#feedback .modal-description"
      ).show();
      $("#feedback .success").hide();
      feedbackStatus = FEEDBACK_STATUSES.send;
    }
    if ($(e.target).closest('#career-video').length === 1) {
      document.querySelector('#career-video video').pause()
    }
  });
  // $("#menu ul a").click(function(e){

  //     // const $anchor = $(this).attr('href')
  //     $("#menu").fadeOut(300);
  //     //  $('html,body').animate({
  //     //            scrollTop: $($anchor).offset().top - 90
  //     //        }, 1000);
  // })
  $(".but").on("click", function (e) {
    e.preventDefault();
    const id = $(this).attr("href");
    $(".but").removeClass("active");
    $(this).addClass("active");
    $(".dropdown-toggle").html($(this).html());
    // $(".section-title").text($(this).text());
    $(".tab-content").hide();
    $(id).show();
  });

  const foodCategories = document.querySelectorAll("[data-category]");
  console.log({ foodCategories });
  foodCategories.forEach((category) => {
    category.onclick = () => {
      document.querySelector(".breadcrumbs a:last-child").textContent =
        category.textContent;
    };
  });

  $("#print-scheme-btn").on("click", handleClickPrintBtn);

  function computeDistances(userCoords) {
    if (!userCoords) return;

    let distances = [];

    window.currentCity.addresses.forEach((value, index) => {
      if (!value.coordinates) return;
      console.log({coords: value.coordinates.split(',')});

      let restCoords = new google.maps.LatLng(...(value.coordinates.split(',')));
      
      console.log({restCoords});

      if (restCoords) {
        let distance 
          = google.maps
          .geometry.spherical
          .computeDistanceBetween(restCoords, userCoords);
        
        console.log(distance)
        distances.push({restaraunt: value, distance});
      }
    });

    console.log({distances})
    return distances;
  }

  async function computeDistance() {
    await loader.load();
    console.log("computing distance...");
    const addrInputVal = $('#dadata-address2').val();

    console.log({addrInputVal});
    if (!addrInputVal) return;

    let request = {
      query: addrInputVal,
      fields: ['name', 'geometry'],
    };
    let userCoords = null;

    console.log({map: window.map});

    let service = new google.maps.places.PlacesService(window.map);
    service.findPlaceFromQuery(request, function(results, status) {
      if (status === google.maps.places.PlacesServiceStatus.OK) {
        userCoords = results[0].geometry.location;
        console.log({results});
        console.log({userCoords});
        let distances = computeDistances(userCoords);
        let nearestRest = {restaraunt: null, distance: Infinity};
        distances.forEach((val)=>{
          if (val.distance < nearestRest.distance) {
            nearestRest = val;
          }
        });

        console.log({nearestRest});
        console.log($("#too-far-delivery-msg"));
        if (nearestRest.distance > 8000) {
          console.log('remove d-none');
          $("#too-far-delivery-msg").removeClass('d-none');
        } else {
          console.log('add d-none');
          $("#too-far-delivery-msg").addClass('d-none');
          $("#checkAddress button.close").trigger('click');
          localStorage.setItem("currentAddress", addrInputVal);
          localStorage.setItem("currentRestaraunt", nearestRest.restaraunt);
          window.location.href = `/set_restaraunt_id?id=${nearestRest.restaraunt.id}`;
        }
      }
    });

    // console.log({userCoords});
    
  }

  $("#checkAddress .submit").on('click', (e) => {
    computeDistance();
    // restaraunts
  });
    
  function handleClickPrintBtn(e) {
    console.log('Clicked')
    let printWin = window.open('', '', 'left=50,top=50,width=800,height=640,toolbar=0,scrollbars=1,status=0');
    const schemesTable = $("#table.admin").clone();
    const prsvg = schemesTable.children('svg')[0];
    
    prsvg.style.width = "100%";
    prsvg.style.height = "100%";
    prsvg.style.transformOrigin = "left top";
    prsvg.style.transform = "scale(1.5, 1.5)";

    schemesTable.html(prsvg.outerHTML);

    let $reservations_info_els = [];
    
    let $reservations_table = $('<table>')
      .css('page-break-before', 'always')
      .css('width', '100%');
        
    $('#new-reservations .cabinet-order').each((ind, el) => {
      let tr = $('<tr>');
      let td1 = $('<td>');
      let td2 = $('<td>').css('text-align', 'center');
      
      let r_table = el.querySelector('.r-table-js').textContent;
      let r_time = el.querySelector('.r-time-js').textContent;
      let r_name = el.querySelector('.r-name-js').textContent;
      let r_phone = el.querySelector('.r-phone-js').textContent;
      
      td1.html(ind+1);
      td2.html(`Столик №${r_table} Время: ${r_time} ` + 
                `${r_name} ${r_phone}`);

      tr.append([td1, td2]);
      console.log({TABLE_ROW: tr});
      $reservations_info_els.push(tr);
    });
    $reservations_table.append($reservations_info_els);

    schemesTable.append($reservations_table);
    let printHtml = schemesTable.html();
    
    printWin.document.write(printHtml);

    printWin.document.close();
    printWin.focus();
    printWin.print();
  };
});
//
