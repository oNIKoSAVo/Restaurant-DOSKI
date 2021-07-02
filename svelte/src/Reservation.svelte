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
    ["January", "Январь"],
    ["February", "Февраль"],
    ["March", "Март"],
    ["April", "Апрель"],
    ["May", "Май"],
    ["June", "Июнь"],
    ["Июль", "Июль"],
    ["August", "Август"],
    ["September", "Сентябрь"],
    ["October", "Октябрь"],
    ["November", "Ноябрь"],
    ["December", "Декабрь"],
  ];

  function validate() {
    console.log("I'm the validate() function");
  }

  async function handleSubmit(e) {
    e.preventDefault();
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
    console.log(response);
  }
</script>

<form on:submit={handleSubmit} preventDefault={validate}>
  Ресторан<br />
  <select bind:value={restaraunt}>
    {#each restaraunts as address}
      <option value={address.id}>
        {address.text}
      </option>
    {/each}
  </select>
  <br /><br />
  <Datepicker format={'#{d}/#{m}/#{Y}'} {daysOfWeek} {monthsOfYear} bind:formattedSelected={date}  />
  <br />
  С
  <input type="text" name="start" bind:value={start} />
  По
  <input type="text" name="end" bind:value={end} /><br /><br />
  Количество человек<br />
  <input type="text" name="persons" bind:value={persons} /><br /><br />
  Стол<br />
  <input type="text" name="table" bind:value={table} /><br /><br />
  Ваше имя<br />
  <input type="text" name="name" bind:value={name} /><br /><br />
  Телефон<br />
  <input type="text" name="phone" bind:value={phone} /><br /><br />
  Пожелание к брони<br />
  <textarea name="description" bind:value={description} /><br /><br />
  <button>Забронировать</button>
</form>

<style>
  .main {
  }
</style>
