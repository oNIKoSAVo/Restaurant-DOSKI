<script>
  import {Datepicker, Swappable} from "svelte-calendar";
  import {request, reservationRequest} from "./api";
  import isNumeric from "validator/es/lib/isNumeric";
  import isAlpha from "validator/es/lib/isAlpha";
  import jquery from "jquery";
  import "dayjs/locale/ru.js";
  import dayjs from "dayjs";
  import CustomDatepicker from "./CustomDatepicker.svelte";
  import Inputmask from "inputmask";
  import {correctTimeWithMask} from "./helpers/correctTimeWithMask";
  import {sendTelegramMessage} from "./helpers/sendTelegramMessage";
  import {captchaProtect} from "./helpers/grecaptcha";
  import {correctPhoneWithMask} from "./helpers/correctPhoneWithMask";
  import {setErrorShadow} from "./helpers/setErrors";
  import isAlphaRuEn from "./helpers/isAlphaRuEn";
  import {isCurrentTimeBetween} from "./helpers/time";
  import {cloneDeep, isEqual} from "lodash-es";
  // const isBetween = require('dayjs/plugin/isBetween')
  import isBetween from 'dayjs/plugin/isBetween'
  import {hasUnderscores} from "./helpers/hasUnderscores";
  import {numbersToPhone} from "./helpers/phoneToNumbers";

  dayjs.extend(isBetween)

  export let restaraunts;
  export let reservation;
  reservation.restaraunt_id = 1;
  let reservationPeriodDays = 10
  let minReservationTime = '12:00';
  let maxReservationTime = '20:00';

  function setCurrentCity(currentCity) {
    window.currentCity = currentCity;
    // const cityChangedEvent = new Event('currentCityChange')
    // window.dispatchEvent(cityChangedEvent)

    window.location.href = `/set_city_id?id=${currentCity.id}`;

    // fetch(`/set_city_id?id=${currentCity.id}`).then(() => document.location.reload())
  }

  window.addEventListener('managerSettingsGet', () => {
    const {
      allow_period_reservation,
      allow_time_reservation_end,
      allow_time_reservation_start
    } = window.managerSettings
    console.log(allow_period_reservation, allow_time_reservation_end, allow_time_reservation_start)

    if (allow_period_reservation) {
      reservationPeriodDays = +allow_period_reservation
      jquery('#allow-period-reservation').textContent = reservationPeriodDays;

      store.getState().end = dayjs().add(reservationPeriodDays, 'day').toDate()
      if (urlSearchParams.get("date")) {

        const [day, month, year] = urlSearchParams.get("date").split("-");
        const maxDate = dayjs().add(reservationPeriodDays, 'day')

        const urlDate = dayjs(`${year}-${month}-${day}`)
        if(!urlDate.isValid()) return

        if (urlDate.isBetween(dayjs().subtract(1, 'day'), maxDate, null, '[]')) {
          store.getState().hasChosen = true
          selectedDate = urlDate.toDate()
          store.getState().selected = urlDate.toDate()
          console.log({store: store.getState()})

        } else {
          // if date in url params is incorrect
          store.getState().hasChosen = false
          store.getState().selected = new Date()
          selectedDate = null
          const emptyModalEl = document.getElementById('empty-modal')
          emptyModalEl.querySelector('.modal-title').textContent = urlDate.isBefore(dayjs().subtract(1, 'day')) ? 'Бронирование на прошедшее время' : 'Бронирование на слишком дальний период'
          openModal('#empty-modal')
        }
      }
    }

    if (allow_time_reservation_end && allow_time_reservation_start) {
      minReservationTime = allow_time_reservation_start.slice(0, -3)
      maxReservationTime = allow_time_reservation_end.slice(0, -3)

      /* create option elements for the select element of available times 
      in the reservation form: */
      // ---------------------------------
      let min = parseInt(minReservationTime);
      let max = parseInt(maxReservationTime);
      const timeSelectEl = document.getElementById('time-selection-field');
      let timeOptions = [];

      console.log('MIN AND MAX: ', min, max);

      for (let h = min; h <= max; h++) {
          const optionEl = document.createElement("option");
          optionEl.classList.add('option');

          let hours = (h).toString().padStart(2,0);
          let timeOption = `${hours}:00`;
          optionEl.setAttribute('value', timeOption);
          optionEl.textContent = timeOption;
          timeOptions.push(optionEl);
      }

      timeSelectEl.append(...timeOptions);
      // ---------------------------------

      if (urlSearchParams.get("time")) {
        const urlTime = urlSearchParams.get("time");
        if (isCurrentTimeBetween(minReservationTime, maxReservationTime, urlTime)) {
          time = urlTime;
        } else {
          const emptyModalEl = document.getElementById('empty-modal')

          if(emptyModalEl.querySelector('.modal-title').textContent.trim()){
            emptyModalEl.querySelector('.modal-title').textContent += '; Неверное время'
          } else {
            emptyModalEl.querySelector('.modal-title').textContent += 'Неверное время'
            openModal('#empty-modal')
          }

        }
      }
    }


    // console.log();
  })
  // console.log({ restaraunt });
  let time = "";
  let persons = "";
  let table = "";
  let name = window.user.name || "";
  let phone = numbersToPhone(window.user.phone) || "";
  let description = "";
  let cityId = localStorage.getItem("chosenCityId");
  let store;
  let tableEls = []
  let showIncorrectPhoneModal = false;

  let responseIdReservation = "";

  export const daysOfWeek = [
    ["Воскресенье", "Вс"],
    ["Monday", "Пн"],
    ["Tuesday", "Вт"],
    ["Wednesday", "Ср"],
    ["Thursday", "Чт"],
    ["Friday", "Пт"],
    ["Saturday", "Cб"],
  ];

  export const monthsOfYear = [
    ["Январь", "Январь"],
    ["Февраль", "Февраль"],
    ["Март", "Март"],
    ["Апрель", "Апрель"],
    ["Май", "Май"],
    ["Июнь", "Июнь"],
    ["Июль", "Июль"],
    ["Август", "Август"],
    ["Сентябрь", "Сентябрь"],
    ["Октябрь", "Октябрь"],
    ["Ноябрь", "Ноябрь"],
    ["Декабрь", "Декабрь"],
  ];

  // const currentCity =
  let restaurantsFromAdmin = [];
  fetch("/restaraunts", {method: "GET"})
          .then((data) => data.json())
          .then((body) => {
            restaurantsFromAdmin = body;
            console.log({body});
          });
  let currentCityRestaurants = [];
  let restaraunt = "";
  $: console.log({restaraunt});


  const urlSearchParams = new URL(window.location.href).searchParams;
  restaraunt = +urlSearchParams.get("restaurant");
  let selectedDate;

  // if (urlSearchParams.get("date")) {
  //   const [day, month, year] = urlSearchParams.get("date").split("-");
  //   console.log({ year });
  //
  //   selectedDate = new Date(+year, +month - 1, +day);
  //   console.log({ restaraunt, selectedDate });
  // }
  // if (urlSearchParams.get("time")) {
  //   const urlTime = urlSearchParams.get("time");
  //   if (correctTimeWithMask(urlTime)) {
  //     time = urlTime;
  //   }
  // }

  window.addEventListener("currentCityChange", (e) => {
    currentCityRestaurants = restaurantsFromAdmin?.filter(
            (el) => el?.city?.name === window.currentCity.name
    );
    if (urlSearchParams.get("restaurant")) {
      const foundRestaurantInCurrentCity = currentCityRestaurants.find(
              (r) => r.id === +urlSearchParams.get("restaurant")
      );
      if (!foundRestaurantInCurrentCity) {
        const foundRestaurantInAllCities = window.restaraunts.find(
                (r) => r.id === +urlSearchParams.get("restaurant")
        );
        if (!foundRestaurantInAllCities) {
          restaraunt = currentCityRestaurants[0]?.id;
        } else {
          console.log({city: foundRestaurantInAllCities.city});
          setCurrentCity(foundRestaurantInAllCities.city);
          localStorage.setItem(
                  "chosenCityName",
                  foundRestaurantInAllCities.city.name
          );
        }
      } else restaraunt = +urlSearchParams.get("restaurant");
    } /*else restaraunt = currentCityRestaurants[0]?.id;*/
    if (!restaraunt) {
      restaraunt = ''
    }
    const schemes = [];
    restaurantsFromAdmin
            .find((r) => r.id === restaraunt)
            ?.schemes.forEach((s) => schemes.push(s));
    appendSchemes(schemes);
  });

  $: if (currentCityRestaurants.length === 0) {
    restaraunt = currentCityRestaurants[0]?.id;
  }

  $: if (store) store.subscribe((storeInfo) => {
    if (storeInfo.hasChosen && !storeInfo.open && !storeInfo.enlargeDay && time) {
      showTableStatus(tableEls)
    }
  })
  $: if (time) {
    showTableStatus(tableEls)
  }
  $: console.log({table});

  document.addEventListener("DOMContentLoaded", () => {
    const im = new Inputmask("99:99");
    const datepicker = im.mask(document.querySelector(".datepicker"));
    // appendSchemes([{url: restaraunts[0]?.schemes[0]?.url}]);
  });

  function slicePeopleForTable(id) {
    let peopleQuantity = "";
    for (let i = 0; i < id.length; i++) {
      peopleQuantity += id[i];
      if (isNaN(+peopleQuantity)) return peopleQuantity.slice(0, -1);
    }
    return peopleQuantity;
  }

  console.log(restaraunts);

  async function handleSubmit(e) {
    e.preventDefault();
    e.stopPropagation();
    console.log({
      restaraunt,
      date: dayjs(store.getState().selected).format("DD/MM/YYYY"),
      time,
      end: time,
      persons,
      table,
      name,
      phone,
      description,
      agreed: document.getElementById("rules").checked,
    });

    // if(lastTableModalTimeout) return
    function setErrorShadowTimed(el) {
      setErrorShadow(el, 5000, 'error-shadow-aggressive')
    }

    if (
            hasUnderscores(time) || !time ||
            !table ||
            !persons ||
            !name ||
            !correctPhoneWithMask(phone) ||
            !restaraunt ||
            !store.getState().hasChosen ||
            !document.getElementById("rules").checked
    ) {
      if (!table) {
        openModal("#table_not_chosen");
      }

      if (!document.getElementById("rules").checked) {
        setErrorShadowTimed(document.querySelector(".rules"));
      }
      if (hasUnderscores(time) || !time) {
        setErrorShadowTimed(document.querySelector("input.datepicker"));
      }
      if (!restaraunt) {
        setErrorShadowTimed(document.querySelector("select[name=restaurant]"));
      }
      // if (!persons) {
      //   setErrorShadowTimed(document.querySelector("input[name=persons]"));
      // }
      if (!name) {
        setErrorShadowTimed(document.querySelector("input[name=name]"));
      }
      if (!correctPhoneWithMask(phone)) {
        setErrorShadowTimed(document.querySelector("input[name=phone]"));
      }

      if (!store.getState().hasChosen) {
        setErrorShadowTimed(document.getElementById("chooseDate"));
      }
      const [maxHours, maxMinutes] = maxReservationTime.split(':')
      const maxDate = dayjs().add(reservationPeriodDays, 'day').add(+maxHours, 'hours').add(+maxMinutes, 'minutes')
      const day = store.getState().day
      const month = store.getState().month
      const year = store.getState().year


      const formDate = dayjs(`${year}-${month + 1}-${day}`)
      const [hours, minutes] = time.split(':')
      const formDateWithHours = formDate.add(+hours, 'hour').add(+minutes, 'minutes')
      const dateNow = dayjs()
      if (!formDateWithHours.isBetween(dateNow, maxDate, null, '[]')) {
        console.log({formDate})
        const emptyModal = document.getElementById('empty-modal')
        emptyModal.querySelector('.modal-title').textContent = formDateWithHours.isBefore(dateNow) ?'Бронирование на прошедшее время' : 'Бронирование на слишком дальний период'
        openModal('#empty-modal')
      }

      // if(!!document.getElementById('rules').checked){
      //     setErrorShadowTimed(document.querySelector('.reserve-form .rules'))
      // }
      return;
    }
    captchaProtect(async () => {


      sendTelegramMessage(
              `${name} забронировал(а) стол ${table} в ${time} на ${persons} человек(а). Номер: ${phone}. Ресторан на улице ${
                      restaraunts.find((el) => el.id === restaraunt).text
              }`
      );

      const response = await reservationRequest({
        restaraunt,
        date: dayjs(store.getState().selected).format("DD/MM/YYYY"),
        time,
        end: time,
        persons,
        table,
        name,
        phone,
        description,
      });

      if (response.id) {
        responseIdReservation = response.id;
        openModal("#reserved");
      } else if (response.status==='error' && response.message){
        const emptyModal = document.getElementById('empty-modal')
        emptyModal.querySelector('.modal-title').textContent = response.message
        openModal("#empty-modal");
      }
    });

    //todo check response
  }

  function handleOnChangeRestaraunt(e) {
    // openModal("#peoplenumber");
    console.log("was here");
    console.log({restaraunts}, {restaraunt});
    const findRestaraunt = restaurantsFromAdmin.find(
            (elem) => elem.id == restaraunt
    );
    appendSchemes(findRestaraunt.schemes);
    // console.log(findRestaraunt);
    // appendSchemes(findRestaraunt.schemes);
    // console.log({ findRestaraunt });
  }

  function openModal(id) {
    jquery(".modal").removeClass("show").hide();
    // saveTop = jquery("html").scrollTop();
    // jquery(".modal-title").text(title);
    // jquery(".modal-subtitle").text(subtitle);
    jquery("html,body").addClass("locked");
    jquery("body").css("overflow", "hidden");
    // jquery("body").css("top", -saveTop);
    document.querySelector(id).style.display = "";
    jquery(id).addClass("show").show();
  }

  async function showTableStatus(restaurantMaps) {
    if (!store?.getState().selected || !restaraunt) {
      return
    }
    const tableNums = (await request('POST', '/reservation?type=check', {
      type: 'check',
      restaraunt,
      date: dayjs(store.getState().selected).format("DD/MM/YYYY"),
      time,
      phone: '-',
      persons: 0,
      table: 0,
      name: 'test',
      description: ''
    })).tables
    table = ''
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


  function appendSchemes(schemes) {
    // if (!document.getElementById("table")) return;
    document.getElementById("table").innerHTML = "";
    tableEls = [];

    schemes.forEach((schema) => {
      let el = document.createElement("svg");
      fetch(schema.url)
              .then((r) => r.text())
              .then((text) => {
                el.innerHTML = text;
                el.class = "svg";
                tableEls.push(el)
                let paths = [...el.querySelectorAll("path")].filter((path) => {
                  if (!isNaN(path.id)) return path;
                });
                const chooseTableBtn = document.querySelector(
                        ".select-table.close-modal"
                );


                paths.forEach((path) =>
                        path.addEventListener("click", function (e) {
                          e.stopPropagation();
                          if (path.classList.contains('reserved')) return
                          openModal("#table-modal");
                          const peopleQuantity = slicePeopleForTable(
                                  this.nextElementSibling.id
                          );
                          document.getElementById(
                                  "table-modal-people-quantity"
                          ).textContent = peopleQuantity;
                          const currentRestaurant = restaraunts.find(
                                  (r) => r.id === restaraunt
                          );
                          const currentTable = currentRestaurant?.tables.find(
                                  (t) => t.table === +path.id
                          );
                            persons = peopleQuantity
                          document
                                  .getElementById("table-modal")
                                  .querySelector(".modal-description").textContent =
                                  currentTable?.description ||
                                  `Столик с видом на город для компании до ${peopleQuantity} человек`;
                          document
                                  .getElementById("table-modal")
                                  .querySelector("img.modal-table").src =
                                  currentTable?.photo || "/static/app/img/table.jpg";
                          document.getElementById("table-modal-number").textContent =
                                  this.id;
                          chooseTableBtn.onclick = () => {
                            paths.forEach((p) => {
                              if (!p.classList.contains('reserved')) p.style.fill = "green"
                            });

                            console.log({
                              sliced: slicePeopleForTable(this.nextElementSibling.id),
                            });

                            table = this.id;
                            this.style.fill = "#7f7f7f";
                            chooseTableBtn.onclick = null;
                          };
                          console.log({el: this});
                        })
                );
              })
              .then(() => {
                if (time && store.getState().selected) showTableStatus(tableEls)
              })
              .then(() => document.getElementById("table").append(...tableEls))

              .catch(console.error.bind(console));
    });


    // showTableStatus()
  }


</script>

<div
  class="modal modal-wrapper fade {showIncorrectPhoneModal ? 'show' : ''}"
  id="correct_time"
  tabindex="-1"
  role="dialog"
>
  <div class="modal-dialog limited" style="max-width: 506px">
    <div class="modal-content">
      <h1>Доступное время бронирования с {minReservationTime} до {maxReservationTime}</h1>
    </div>
  </div>
</div>

<div
  class="modal modal-wrapper fade {responseIdReservation != '' ? 'show' : ''}"
  id="reserved"
  tabindex="-1"
  role="dialog"
>
  <div class="modal-dialog limited" style="max-width: 506px">
    <div class="modal-content">
      <button
        class="close"
        type="button"
        data-dismiss="modal"
        aria-label="Close"
      >
        <span aria-hidden="true">&times;</span>
      </button>
      <div class="modal-subtitle mt-1 mb-2">{responseIdReservation}</div>
      <div class="modal-header">
        <div class="modal-title">СФОТОГРАФИРУЙТЕ ИЛИ СОХРАНИТЕ НОМЕР БРОНИ</div>
      </div>
      <div class="modal-description">для предъявления его в заведении</div>
      <div class="text-center">
        <a class="mt-0 mb-3 submit" href="#askpreorder" data-modal>ОК</a>
      </div>
    </div>
  </div>
</div>

<form id="reserve-form" on:submit={handleSubmit}>
  <div class="row">
    <div class="col-12 d-sm-block">
      <!-- svelte-ignore a11y-no-onchange -->
      <select
        bind:value={restaraunt}
        on:change={handleOnChangeRestaraunt}
      >
        <option value="">Выберите ресторан</option>
        {#each currentCityRestaurants as restaurant}
          <option value={restaurant.id}>
            {restaurant.address}
          </option>
        {/each}
      </select>
    </div>
    <div class="col-5">
      <CustomDatepicker
        bind:store
        start="{dayjs()}"
        end="{dayjs().add(reservationPeriodDays, 'day')}"
        bind:selected="{selectedDate}"
      />
    </div>
    <!-- <div class="col-7">
      <input
        class="datepicker"
        type="text"
        placeholder="Время"
        on:change={(e) => {
          if (!isCurrentTimeBetween( minReservationTime, maxReservationTime, e.target.value)) {
            e.target.value = "";
            showIncorrectPhoneModal = true;
            const errorTimeModal = document.getElementById("correct_time");
            errorTimeModal.style.display = "";
            setTimeout(() => {
              errorTimeModal.onclick = () => {
                showIncorrectPhoneModal = false;
                errorTimeModal.onclick = null;
              };
            });
          } else {
            time = e.target.value;
          }
        }}
        value="{time}"
      />
    </div> -->
    <div class="col-7 d-sm-block">
      <select
              class="select"
              id="time-selection-field"
              on:change={(e) => {
                time = e.target.value;
              }}
      >
          <option value='' class="option">
              Выберите время
          </option>
      </select>
    </div>
    <!-- <div class="col-md-6">
      <select
        name="persons"
        bind:value={persons}
        placeholder="Количество человек"
      >
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
        <option value="6">6</option>
      </select>
    </div> -->
    <div class="col-sm-6">
      <input
        name="name"
        placeholder="Ваше имя"
        value={name}
        on:input={(e) => {
          if (isAlpha(e.target.value, "ru-RU") || e.target.value === "") {
            name = e.target.value;
          } else {
            e.target.value = name;
          }
        }}
      />
    </div>
    <div class="col-sm-6">
      <input
        type="text"
        name="table"
        placeholder="Стол"
        value={table}
        disabled
        on:change={(e) => {
          let paths = [...document.querySelectorAll("path")].filter((path) => {
            if (!isNaN(path.id)) return path;
          });
          paths.forEach((r) => (r.style.fill = "green"));
          document.getElementById(table).style.fill = "#7f7f7f";
        }}
      /></div>
      <div class="col-sm-12">
      <input
        class="phone-input"
        name="phone"
        on:change={(e) => (phone = e.target.value)}
        value="{phone}"
        placeholder="Номер телефона для связи"
      />
    </div>
    <div class="col-12">
      <textarea
        name="message"
        rows="8"
        placeholder="Пожелания к брони..."
        bind:value={description}
      />
    </div>
    <div class="col-12 rules">
      <input type="checkbox" id="rules" /> <label for="rules" /><a
        id="visit_rules"
        href="#">C правилами посещения</a
      >&nbsp;ознакомлен
    </div>

    <div class="col-12">
      <a class="submit" href="#" on:click={handleSubmit}>Забронировать</a>
    </div>
  </div>
</form>

<style>
  .svelte-1lorc63 {
    width: 200px;
  }
</style>
