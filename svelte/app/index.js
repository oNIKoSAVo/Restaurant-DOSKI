import "./index.scss";
import $ from "jquery";
import "lazysizes";
import Modal from "modal-vanilla";
import Parallax from "parallax-js";
import SwiperCore, { Navigation, Pagination, Swiper } from "swiper/core";
// import Swiper styles
import "swiper/swiper-bundle.css";
import Inputmask from "inputmask";
import "lazysizes/plugins/parent-fit/ls.parent-fit";
import "./plugin/grt-youtube-popup";
// import datepicker from "js-datepicker";
import "regenerator-runtime/runtime.js";

import { Loader } from "google-maps";
import { correctPhoneWithMask } from "../src/helpers/correctPhoneWithMask";
import { sendTelegramMessage } from "../src/helpers/sendTelegramMessage";
import {captchaProtect} from "../src/helpers/grecaptcha";
const options = {
  /* todo */
};

const loader = new Loader("AIzaSyCMyW6HJLx8TXMlSemVjqMQkhb7-Bz8tGI", options);
SwiperCore.use([Navigation, Pagination]);

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

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    submitJobForm();
    return false;
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
function initMap() {
  var center = new google.maps.LatLng(54.964361, 82.93014);

  if (detectmob()) {
    center = new google.maps.LatLng(54.962361, 82.92694);
  }
  var factory = new google.maps.LatLng(54.962361, 82.93014);
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
      div.innerHTML =
        '<div class="iw-title">ооо «СТМ-КОСМЕТИКА»</div>' +
        '<div class="iw-content">' +
        '<div class="iw-subTitle">г. Новосибирск,<br/>проспект Мира, 62</div>' +
        '<p style="margin-top:4px;"><a href="tel:+7(383)247-7929">+7 (383) 247-7929</a><a href="mailto:anton@stm-cosmetics.ru">anton@stm-cosmetics.ru</a></p>';
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
    if ($(this).next().hasClass("code-input")) $(this).next().trigger("focus");
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
    })


  });
  $(".checkout-btn").on("click", function (e) {
    const cartSummaryEl = document.querySelector(".cart-summary");
    if (cartSummaryEl) {
      if (+cartSummaryEl.textContent.slice(0, -2) < 500) return;
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
  $("#nextBtn").on("click", function (e) {
    const regForm = document?.getElementById("regForm");
    // const whereWantToWork = document?.getElementById("whereWantToWork");
    const jobModal = e.target.closest("#jobmodal");
    const isJobModal = !!jobModal;
    if (isJobModal) {
      if (!correctPhoneWithMask(jobModal.querySelector(".phone-input").value)) {
        setErrorShadow(jobModal.querySelector(".phone-input"));
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
    if (
      e.target.textContent === "Отправить" ||
      !regForm?.querySelector("#rules").checked
    )
      return;
    nextPrev(1);
  });
  $("#prevBtn").on("click", function () {
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
    $(
      "#feedback .modal-title,#feedback a,#feedback input,#feedback textarea,#feedback .modal-description"
    ).hide();
    $("#feedback .success").show();
  });
  $(".only-menu .dish-item").on("click", function () {
    openModal("#item");
  });
  function setModalData(modal, dishItem){
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
        dishItem.querySelector(".dish-details_sizes").textContent + ' /';
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
    setModalData(modal, dishItem)
    openModal("#item-buy");

  });
  $(".delete-account").on("click", function (e) {
    e.preventDefault();
    // Удаление аккаунта

    // Успешный исход
    $("#deleteaccount .modal-title,#deleteaccount a").hide();
    $("#deleteaccount .success").show();
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
  $("a[data-modal]").on("click", function (e) {
    e.preventDefault();
    openModal($(this).attr("href"));
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
    if ($(event.target).hasClass("modal-wrapper")) {
      $(".modal-wrapper").fadeOut(400);
      $("html,body").removeClass("locked");
      $("body").css("overflow", "auto");
      $("html").scrollTop(saveTop);
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
    $(".section-title").text($(this).text());
    $(".tab-content").hide();
    $(id).show();
  });

  const foodCategories = document.querySelectorAll('[data-category]')
  console.log({foodCategories})
  foodCategories.forEach(category => {
    category.onclick = () => {
      document.querySelector('.breadcrumbs a:last-child').textContent = category.textContent
    }
  })
});
//
