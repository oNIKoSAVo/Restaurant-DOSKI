<script>
  import Datepicker from "svelte-calendar";
  import { reservationRequest } from "./api";

  export let restaraunts;

  let restaraunt = "";
  let date = "";
  let start = "";
  let end = "";
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

  function validate() {
    console.log("I'm the validate() function");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    e.stopPropagation();

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
    console.log(restaraunts);
    const findRestaraunt = restaraunts.find(elem => elem.id == restaraunt);
    console.log(findRestaraunt)
    appendSchemes(findRestaraunt.schemes);
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
          let rects = document.querySelectorAll("rect.cls-5");
          console.log({ rects });
          rects.forEach((rect) =>
            rect.addEventListener("click", function () {
              rects.forEach((r) => (r.style.fill = "green"));
              table = rect.nextSibling.textContent;
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
        format={"#{d}/#{m}/#{Y}"}
        {daysOfWeek}
        {monthsOfYear}
        bind:formattedSelected={date}
      />
    </div>
    <div class="col-md-3 col-6">
      <input placeholder="От" bind:value={start} />
    </div>
    <div class="col-md-3 col-6">
      <input placeholder="До" bind:value={end} />
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
      <input name="name" placeholder="Ваше имя" bind:value={name} />
    </div>
    <div class="col-12">
      <input
        type="text"
        name="table"
        placeholder="Стол"
        bind:value={table}
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
