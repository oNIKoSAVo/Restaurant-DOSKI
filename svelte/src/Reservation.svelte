<script>
  import Datepicker from "svelte-calendar";
  import { reservationRequest } from "./api";
  import isNumeric from "validator/es/lib/isNumeric";
  import isAlpha from "validator/es/lib/isAlpha";
  import jquery from "jquery";

  export let restaraunts;
  export let reservation;

  let restaraunt = reservation.restaraunt_id
    ? parseInt(reservation.restaraunt_id)
    : "";
  let date = "";
  let start = "00:00";
  let end = "00:00";
  let persons = "";
  let table = "";
  let name = "";
  let phone = "";
  let description = "";

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

  // function validate(e, validateFn, stateValue) {
  //   if (validateFn(e.target.value) || e.target.value === "") {
  //     stateValue = e.target.value;
  //   } else {
  //     e.target.value = stateValue;
  //   }
  // }

  document.addEventListener("DOMContentLoaded", () => {
    appendSchemes([{ url: restaraunts[0]?.schemes[0]?.url }]);
  });

  function slicePeopleForTable(id) {
    let peopleQuantity = "";
    for (let i = 0; i < id.length; i++) {
      peopleQuantity += id[i];
      if (isNaN(+peopleQuantity)) return peopleQuantity.slice(0, -1);
    }
    return peopleQuantity;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    e.stopPropagation();
    openModal("#askpreorder");
    const response = await reservationRequest({
      restaraunt,
      date,
      start,
      end,
      persons,
      table,
      name,
      phone,
      description,
    });
    if (response.id) {
      responseIdReservation = response.id;
    }
  }

  function handleOnChangeRestaraunt(e) {
    // openModal("#peoplenumber");

    console.log(restaraunts);
    const findRestaraunt = restaraunts.find((elem) => elem.id == restaraunt);
    console.log(findRestaraunt);
    // appendSchemes(findRestaraunt.schemes);
    console.log({ findRestaraunt });
    appendSchemes([{ url: findRestaraunt.schemes[0]?.url }]);
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

          paths.forEach((path) =>
            path.addEventListener("click", function (e) {
              e.stopPropagation();
              paths.forEach((r) => (r.style.fill = "green"));
              openModal("#table-modal");
              document.getElementById(
                "table-modal-people-quantity"
              ).textContent = slicePeopleForTable(this.nextElementSibling.id);
              console.log({
                sliced: slicePeopleForTable(this.nextElementSibling.id),
              });
              console.log({ el: this });
              document.getElementById("table-modal-number").textContent =
                this.id;
              table = this.id;
              this.style.fill = "#7f7f7f";
            })
          );
        })
        .catch(console.error.bind(console));
    });
  }
</script>

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

<form id="reserve-form">
  <div class="row">
    <div class="col-12 d-none d-sm-block">
      <!-- svelte-ignore a11y-no-onchange -->
      <select bind:value={restaraunt} on:change={handleOnChangeRestaraunt}>
        {#each restaraunts as address}
          <option value={address.id}>
            {address.text}
          </option>
        {/each}
      </select>
    </div>
    <div class="col-sm-6 svelte-1lorc63">
      <Datepicker
        selected={reservation.date
          ? new Date(
              reservation.date.replace(/(\d{2})-(\d{2})-(\d{4})/, "$3-$2-$1")
            )
          : new Date()}
        format={"#{d}/#{m}/#{Y}"}
        {daysOfWeek}
        {monthsOfYear}
        bind:formattedSelected={date}
      />
    </div>
    <div class="col-md-3 col-6">
      <input
        placeholder="От"
        value={start}
        on:input={(e) => {
          if (!e.target.value.includes(":") || e.target.value.length > 5) {
            start = `00:00`;
            e.target.value = start;
            return;
          }

          const [hours, minutes] = e.target.value.split(":");
          if (hours.trim() !== "") {
            if (!isNumeric(hours) || +hours > 23) {
              start = `00:${start.slice(2)}`;
              e.target.value = start;
              return;
            }
          }

          if (minutes.trim() !== "") {
            if (!isNumeric(minutes) || +minutes > 59) {
              start = `${start.slice(0, 2)}:00`;
              e.target.value = start;
              return;
            }
          }

          start = e.target.value;
        }}
      />
    </div>
    <div class="col-md-3 col-6">
      <input
        placeholder="До"
        value={end}
        on:input={(e) => {
          if (!e.target.value.includes(":") || e.target.value.length > 5) {
            end = `00:00`;
            e.target.value = end;
            return;
          }

          const [hours, minutes] = e.target.value.split(":");
          if (hours.trim() !== "") {
            if (!isNumeric(hours) || +hours > 23) {
              end = `00:${end.slice(2)}`;
              e.target.value = end;
              return;
            }
          }

          if (minutes.trim() !== "") {
            if (!isNumeric(minutes) || +minutes > 59) {
              end = `${end.slice(0, 2)}:00`;
              e.target.value = end;
              return;
            }
          }

          end = e.target.value;
        }}
      />
    </div>
    <div class="col-md-6">
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
    </div>
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
    <div class="col-12">
      <input
        type="text"
        name="table"
        placeholder="Стол"
        value={table}
        on:input={(e) => {
          if (isNumeric(e.target.value) || e.target.value === "") {
            table = e.target.value;
          } else {
            e.target.value = table;
          }
        }}
        on:change={(e) => {
          let paths = [...document.querySelectorAll("path")].filter((path) => {
            if (!isNaN(path.id)) return path;
          });
          paths.forEach((r) => (r.style.fill = "green"));
          document.getElementById(table).style.fill = "#7f7f7f";
        }}
      /><br /><br />
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
      <input id="rules" type="checkbox" /> <label for="rules" /><a href="#"
        >C правилами посещения</a
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
