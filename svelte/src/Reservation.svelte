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

  export let restaraunts;
  export let reservation;
  reservation.restaraunt_id = 1;

  function setCurrentCity(currentCity){
    window.currentCity = currentCity
    // const cityChangedEvent = new Event('currentCityChange')
    // window.dispatchEvent(cityChangedEvent)

    window.location.href = `/set_city_id?id=${currentCity.id}`

    // fetch(`/set_city_id?id=${currentCity.id}`).then(() => document.location.reload())
  }

  // console.log({ restaraunt });
  let time = "";
  let persons = "";
  let table = "";
  let name = window.user.name || "";
  let phone = "";
  let description = "";
  let cityId = localStorage.getItem('chosenCityId')
  let store;

  let showIncorrectPhoneModal = false

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
  let restaurantsFromAdmin = []
  fetch('/restaraunts', {method: 'GET'}).then((data) => data.json()).then(body => {
    restaurantsFromAdmin = body
    console.log({body})
  })
  let currentCityRestaurants = []
  let restaraunt = ''
  $: console.log({restaraunt})
  const urlSearchParams = new URL (window.location.href).searchParams
  restaraunt = +urlSearchParams.get('restaurant')
  let selectedDate;

  if(urlSearchParams.get('date')){
    const [day, month, year] = urlSearchParams.get('date').split('-')
    console.log({year})
    selectedDate = new Date(+year, +month - 1, +day)
    console.log({restaraunt, selectedDate})
  }
  if(urlSearchParams.get('time')){
    const urlTime = urlSearchParams.get('time')
    if(correctTimeWithMask(urlTime)){
      time = urlTime
    }
  }

$:    console.log({currentCityRestaurants})

  window.addEventListener('currentCityChange', e => {
    currentCityRestaurants = restaurantsFromAdmin?.filter((el) => el?.city?.name === window.currentCity.name)
    if(urlSearchParams.get('restaurant')){
      const foundRestaurantInCurrentCity = currentCityRestaurants.find(r => r.id === +urlSearchParams.get('restaurant'))
      if(!foundRestaurantInCurrentCity) {
        const foundRestaurantInAllCities = window.restaraunts.find(r => r.id === +urlSearchParams.get('restaurant'))
        if(!foundRestaurantInAllCities){
          restaraunt = currentCityRestaurants[0]?.id
        }
        else {
          console.log({city: foundRestaurantInAllCities.city})
          setCurrentCity(foundRestaurantInAllCities.city)
          localStorage.setItem("chosenCityName", foundRestaurantInAllCities.city.name);
        }
      }
      else restaraunt = +urlSearchParams.get('restaurant')
    }
    // else restaraunt = currentCityRestaurants[0]?.id
    if(!restaraunt){
      restaraunt = ''
    }
    const schemes = []
    restaurantsFromAdmin.find(r => r.id === restaraunt)?.schemes.forEach(s => schemes.push(s))
    appendSchemes(schemes);
  })


  $: if (currentCityRestaurants.length === 0) {
    restaraunt = currentCityRestaurants[0]?.id
  }
  $: console.log({table})
  // restaraunt = currentCityRestaurants[0]?.address;
  // function validate(e, validateFn, stateValue) {
  //   if (validateFn(e.target.value) || e.target.value === "") {
  //     stateValue = e.target.value;
  //   } else {
  //     e.target.value = stateValue;
  //   }
  // }
  document.addEventListener("DOMContentLoaded", () => {
    const im = new Inputmask("99:99");
    const datepicker = im.mask(document.querySelector("input.timepicker"));
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
      date: dayjs(store.getState().selected).format('DD/MM/YYYY'),
      time,
      end: time,
      persons,
      table,
      name,
      phone,
      description,
      agreed: document.getElementById('rules').checked
    })
    // if(lastTableModalTimeout) return
    if (!correctTimeWithMask(time) || !table || !persons || !name || !correctPhoneWithMask(phone) || !restaraunt || !store.getState().hasChosen || !document.getElementById('rules').checked) {
      if(!table) {
        setErrorShadow(document.querySelector('input[name=table]'))
      }
      if(!correctTimeWithMask(time)){
        setErrorShadow(document.querySelector('input.timepicker'))
      }
      if(!persons){
        setErrorShadow(document.querySelector('select[name=persons]'))
      }
      if(!name){
        setErrorShadow(document.querySelector('input[name=name]'))
      }
      if(!correctPhoneWithMask(phone)){
        setErrorShadow(document.querySelector('input[name=phone]'))
      }

      if(!store.getState().hasChosen) {
        setErrorShadow(document.getElementById('chooseDate'))
      }

      // if(!!document.getElementById('rules').checked){
      //     setErrorShadow(document.querySelector('.reserve-form .rules'))
      // }
      return
    }
    captchaProtect(async () => {
      openModal("#askpreorder");

      sendTelegramMessage(`${name} забронировал(а) стол ${table} в ${time} на ${persons} человек(а). Номер: ${phone}. Ресторан на улице ${
              restaraunts.find((el) => el.id === restaraunt).text
      }`)

      const response = await reservationRequest({
        restaraunt,
        date: dayjs(store.getState().selected).format('DD/MM/YYYY'),
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
      }
    })

    //todo check response
  }

  function handleOnChangeRestaraunt(e) {
    // openModal("#peoplenumber");
    console.log("was here");
    console.log({restaraunts}, {restaraunt});
    const findRestaraunt = restaurantsFromAdmin.find((elem) => elem.id == restaraunt);
    console.log(findRestaraunt);
    // appendSchemes(findRestaraunt.schemes);
    console.log({findRestaraunt});
    appendSchemes(findRestaraunt.schemes);
  }

  function openModal(id) {
    jquery(".modal").removeClass("show").hide();
    // saveTop = jquery("html").scrollTop();
    // jquery(".modal-title").text(title);
    // jquery(".modal-subtitle").text(subtitle);
    jquery("html,body").addClass("locked");
    jquery("body").css("overflow", "hidden");
    // jquery("body").css("top", -saveTop);
    jquery(id).addClass("show").show();
  }

  function appendSchemes(schemes) {
    // if (!document.getElementById("table")) return;
    document.getElementById("table").innerHTML = "";
    schemes.forEach((schema) => {
      let el = document.createElement("svg");
      fetch(schema.url)
              .then((r) => r.text())
              .then((text) => {
                el.innerHTML = text;
                el.class = "svg";
                document.getElementById("table").appendChild(el);
                let paths = [...document.querySelectorAll("path")].filter((path) => {
                  if (!isNaN(path.id)) return path;
                });
                const chooseTableBtn = document.querySelector('.select-table.close-modal')

                paths.forEach((path) =>
                        path.addEventListener("click", function (e) {
                          e.stopPropagation();
                          openModal("#table-modal");
                          const peopleQuantity = slicePeopleForTable(
                                  this.nextElementSibling.id
                          );
                          document.getElementById(
                                  "table-modal-people-quantity"
                          ).textContent = peopleQuantity;
                          const currentRestaurant = restaraunts.find(r => r.id === restaraunt)
                          const currentTable = currentRestaurant.tables.find(t => t.table === +path.id)
                          persons = peopleQuantity
                          console.log({currentTable})
                          document
                                  .getElementById("table-modal")
                                  .querySelector(
                                          ".modal-description"
                                  ).textContent = currentTable?.description || `Столик с видом на город для компании до ${peopleQuantity} человек`;
                          document.getElementById('table-modal').querySelector('img.modal-table').src = currentTable?.photo || '/static/app/img/table.jpg'
                          document.getElementById("table-modal-number").textContent =
                                  this.id;
                          console.log({restaraunttt: restaraunts})
                          chooseTableBtn.onclick = () => {
                            paths.forEach((r) => (r.style.fill = "green"));

                            console.log({
                              sliced: slicePeopleForTable(this.nextElementSibling.id),
                            });


                            table = this.id;
                            this.style.fill = "#7f7f7f";
                            chooseTableBtn.onclick = null
                          }
                          console.log({el: this});

                        })
                );
              })
              .catch(console.error.bind(console));
    });
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
      <h1>Доступное время бронирования с 12.00 до 20.00</h1>
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
        selected="{selectedDate}"
      />
    </div>
    <div class="col-7">
      <select  on:change={(e) => {
          if (!correctTimeWithMask(e.target.value)) {
            e.target.value = "";
            showIncorrectPhoneModal = true;
            setTimeout(() => {
              showIncorrectPhoneModal = false;
            }, 3000);
          } else {
            time = e.target.value;
          }
        }}>
        <option value="12:00" selected>12:00</option>
        <option value="12:30" >12:30</option>
        <option value="13:00" >13:00</option>
        <option value="13:30" >13:30</option>
        <option value="14:00" >14:00</option>
        <option value="14:30" >14:30</option>
        <option value="15:00" >15:00</option>
        <option value="15:30" >15:30</option>
        <option value="16:00" >16:00</option>
        <option value="16:30" >16:30</option>
        <option value="17:00" >17:00</option>
        <option value="17:30" >17:30</option>
        <option value="18:00" >18:00</option>
        <option value="18:30" >18:30</option>
        <option value="19:00" >19:00</option>
        <option value="19:30" >19:30</option>
        <option value="20:00" >20:00</option>
      </select>
<!--      <input-->
<!--        placeholder="Время"-->
<!--        class="timepicker"-->


<!--      />-->
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
