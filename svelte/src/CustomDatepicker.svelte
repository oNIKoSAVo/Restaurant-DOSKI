<script>
  import { Datepicker } from "svelte-calendar";
  import dayjs from "dayjs";
  import "dayjs/locale/ru.js";

  export let store;
  export let options;

  let locale = "ru";

  $: dayjs.locale(locale);
</script>

<Datepicker
  on:mouseover={() => {
    document.body.classList.add("locked");
  }}
  bind:store
  let:key
  let:send
  let:receive
  theme={{
    calendar: {
      width: "500px",
      font: {
        large: "20em",
      },
    },
  }}
>
  <button
    id="chooseDate"
    class={options?.classList || ""}
    in:receive|local={{ key }}
    out:send|local={{ key }}
    on:click={() => {
      document.body.classList.add("locked");
      document.onclick = (e) => {
        if (e.target.closest(".sc-popover") && !(e.target?.hash === "#pickday"))
          return;
        document.body.classList.remove("locked");

        document.onclick = null;
      };
    }}
  >
    {#if $store?.hasChosen}
      {dayjs($store.selected).format("ddd MMM D, YYYY")}
    {:else}
      Выберите дату
    {/if}
  </button>
</Datepicker>

<style>
  button {
    background: white;
    border: 1px solid #e8e8e8;
    color: #444;
    padding: 18px 30px;
    width: 100%;
    font-size: 1.2em;
    border-radius: 6px;
    cursor: pointer;
    font-family: "Muller", sans-serif;
  }
</style>
