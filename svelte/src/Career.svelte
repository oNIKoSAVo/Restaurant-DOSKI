<script>
  import { Datepicker } from "svelte-calendar";
  import { careerRequest } from "./api";
  import CustomDatepicker from "./CustomDatepicker.svelte";
  import isAlpha from "validator/es/lib/isAlpha";
  import dayjs from "dayjs";
  import {captchaProtect} from "./helpers/grecaptcha";
  let showModal = false;
  let showFormModal = true;
  let showModalSuccess = false;
  let first_name = "";
  let middle_name = "";
  let last_name = "";
  let phone = "";
  let position = "";
  let cityId = localStorage.getItem('chosenCityId') || '';
  let bar = "";
  let b_day = "";
  let citizenship = "";
  let about = "";
  let datepickerError = false
  let store;
  $: console.log(showModalSuccess);
  $: console.log(showFormModal);
  $: console.log(showModal);
  let cities = []
  window.addEventListener('currentCityChange', e => {
    cities = window.cities
  })
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
    if(!store.getState().hasChosen) {
      datepickerError = true
      setTimeout(() => {datepickerError=false}, 3000)
      return
    }

    captchaProtect(async () => {
      const formatted = dayjs(store.getState().selected).format("DD/MM/YYYY");
      b_day = formatted.split(".").reverse().join("-");
      const response = await careerRequest({
        first_name,
        middle_name,
        last_name,
        phone,
        position,
        city: cityId,
        bar,
        b_day,
        citizenship,
        about,
      });
      console.log(response.status, response.status == "success");
      if (response.status == "success") {
        showFormModal = false;
        showModalSuccess = true;
        showModal = true;
      }
    })

  }
  function handleNextClick(e) {
    if (e.target.innerHTML == "Отправить") handleSubmit(e);
  }
  document.querySelector("#jobmodal-btn").addEventListener("click", (e) => {
    showModal = true;
  });

</script>

<div
        class="modal-wrapper modal fade {showModal &&
  showFormModal &&
  !showModalSuccess
    ? 'show'
    : ''}"
        id="jobmodal"
        tabindex="-1"
        role="dialog"
        style={showModal ? "display: block" : ""}
        on:click|stopPropagation={(e) => {
    if (e.target.classList.contains("modal-wrapper")) {
      showModal = false;
    }
  }}
>
  <div class="modal-dialog" style="max-width: 747px">
    <div class="modal-content">
      <button
              class="close"
              type="button"
              data-dismiss="modal"
              aria-label="Close"
              on:click={() => (showModal = showFormModal = false)}
      >
        <span aria-hidden="true">&times;</span>
      </button>
      <div class="d-flex justify-content-between align-items-center">
        <span class="step">Шаг 1</span><span class="step">Шаг 2</span><span
              class="step">Шаг 3</span
      >
      </div>
      <div class="modal-header pb-4 pt-0 success">
        <div class="modal-title text-left">Заявка успешно отправлена</div>
      </div>
      <p class="modal-description success">
        С тобой свяжутся в ближайшее время
      </p>
      <form id="regForm" action="">
        <div class="tab row">
          <div class="tab-title col-12">КАК ТЕБЯ ЗОВУТ?</div>
          <div class="col-sm-4">
            <input
                    placeholder="Имя"
                    value={first_name}
                    class="first_name"
                    on:input={(e) => {
                if (
                  isAlpha(e.target.value, "ru-RU", { ignore: "s" }) ||
                  e.target.value === ""
                ) {
                  first_name = e.target.value;
                } else {
                  e.target.value = first_name;
                }
              }}
            />
          </div>
          <div class="col-sm-4">
            <input
                    placeholder="Фамилия"
                    value={last_name}
                    class="last_name"
                    on:input={(e) => {
                if (
                  isAlpha(e.target.value, "ru-RU", { ignore: "s" }) ||
                  e.target.value === ""
                ) {
                  last_name = e.target.value;
                } else {
                  e.target.value = last_name;
                }
              }}
            />
          </div>
          <div class="col-sm-4">
            <input
                    placeholder="Отчество"
                    value={middle_name}
                    class="middle_name"
                    on:input={(e) => {
                if (
                  isAlpha(e.target.value, "ru-RU", { ignore: "s" }) ||
                  e.target.value === ""
                ) {
                  middle_name = e.target.value;
                } else {
                  e.target.value = middle_name;
                }
              }}
            />
          </div>
          <div class="col-12">
            <input
                    class="phone-input"
                    placeholder="Телефон"
                    bind:value={phone}
            />
          </div>
          <div class="col-12 rules">
            <input id="rules" type="checkbox" /> <label for="rules" /><a
                  href="#consent_processing_data_modal"
                  data-modal on:click={() => showModal = false}>Согласие на обработку персональных данных</a
          >
          </div>
        </div>
        <div class="tab row" id="whereWantToWork">
          <div class="tab-title col-12">ГДЕ ХОЧЕШЬ РАБОТАТЬ</div>
          <div class="col-12">
            <select name="job" bind:value={position}>
              <option value="">Выбери должность</option>
              <option value="Бармен">Бармен</option>
              <option value="Повар">Повар</option>
              <option value="Менеджер смены">Менеджер смены</option>
              <option value="Сотрудник охраны">Сотрудник охраны</option>
              <option value="Хостес ">Хостес </option>
              <option value="Администратор">Администратор</option>
              <option value="Официант">Официант</option>
            </select>
          </div>
          <div class="col-12">
            <select name="city" bind:value={cityId}>
              <option value="">Выбери город</option>
              {#each cities as city}
                {(city.id === localStorage.getItem('chosenCityId'))}
                <option value="{city.id}" >{city.name}</option>
              {/each}
            </select>
          </div>
        </div>
        <div class="tab row">
          <div class="tab-title col-12">Пара слов о себе</div>
          <!--          <div class="col-12">-->
          <div
                  class="col-6"
                  style="position: relative"
                  on:click={() => console.log(store.getState().selected)}
          >
            <CustomDatepicker
                    bind:store
                    options={{ classList: `mb-3 w-100 ${datepickerError ? 'error-shadow' : ''}`, color: "#000" }}
                    theme={{ width: "300px" }}
                    unselectedText="Дата рождения"
            />
          </div>
          <!--          </div>-->
          <div class="col-12">
            <textarea placeholder="Расскажи о себе" bind:value={about} style="padding-left: 5px;"/>
          </div>
        </div>
        <div
                class="
          text-center
          d-flex
          justify-content-between
          align-items-center
        "
        >
          <a class="download mr-2 active" id="prevBtn" href="#">Назад</a>
          <div class="d-flex justify-content-end w-100"><a
                  class="submit ml-2"
                  id="nextBtn"
                  on:click={handleNextClick}
                  href="#">Далее</a
          ><a class="submit success close-modal" href="#">ОК</a></div>
        </div>
      </form>
    </div>
  </div>
</div>

<div
        class="modal modal-wrapper fade {showModal &&
  showModalSuccess &&
  !showFormModal
    ? 'show'
    : ''}"
        tabindex="-1"
        role="dialog"
        on:click|stopPropagation={(e) => {
    if (e.target.classList.contains("modal-wrapper")) {
      showModal = false;
    }
  }}
>
  <div class="modal-dialog" style="max-width: 484px">
    <div class="modal-content">
      <button
              class="close"
              type="button"
              data-dismiss="modal"
              aria-label="Close"
              on:click={() => (showModal = false)}
      >
        <span aria-hidden="true">&times;</span>
      </button>
      <div class="modal-header mt-3">
        <div class="modal-title text-left text-sm-center">
          Заявка успешно отправлена
        </div>
      </div>
      <p class="modal-description">С тобой свяжутся в ближайшее время</p>
      <div class="pb-3 text-center">
        <a
                class="submit close-modal"
                href="#"
                on:click={() => (showModal = false)}>Ок</a
        >
      </div>
    </div>
  </div>
</div>

<!--
<form on:submit={handleSubmit} preventDefault={validate}>
  <br/> ----------- <br/>
  Фамилия<br />
  <input type="text" name="name" bind:value={last_name} /><br />
  Имя<br />
  <input type="text" name="name" bind:value={first_name} /><br />
  Отчество<br />
  <input type="text" name="name" bind:value={middle_name} /><br />
  Телефон<br />
  <input type="text" name="phone" bind:value={phone} /><br />
  <br/> ----------- <br/>
  Должность<br />
  <input type="text" name="position" bind:value={position} /><br />
  Город<br />
  <input type="text" name="city" bind:value={city} /><br />
  Бар<br />
  <input type="text" name="bar" bind:value={bar} /><br />
  <br/> ----------- <br/>
  Дата рождения<br />
  <input type="text" name="b_day" bind:value={b_day} /><br />
  Гражданство<br />
  <input type="text" name="citizenship" bind:value={citizenship} /><br />
  О себе<br />
  <textarea name="about" bind:value={about} /><br />
  <button>Отправить</button>
</form> -->
<style>
  .svelte-1lorc63 {
    width: 200px;
  }
</style>
