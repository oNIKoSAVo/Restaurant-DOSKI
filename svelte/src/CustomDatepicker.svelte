<script>
  import {Datepicker} from "svelte-calendar";
  import dayjs from "dayjs";
  import "dayjs/locale/ru.js";

  export let store;
  export let options;
  export let theme;
  export let unselectedText
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
      width: theme?.width ?? "500px",
      font: {
        large: "20em",
      },
    },
  }}
>
  <button
          style={`color: ${options?.color ?? "rgba(255, 255, 255, 0.7)"}`}
          id="chooseDate"
          className={options?.classList || ""}
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
      {unselectedText || 'Выберите дату'}
    {/if}
  </button>
</Datepicker>

<style>
  button {
    background: transparent;
    border: 1px solid rgba(190, 190, 190, 0.5);
    padding: 18px 15px;
    width: 100%;
    font-size: 1.2em;
    border-radius: 6px;
    cursor: pointer;
    font-family: "Muller", sans-serif;
  }

  @media (max-width: 1200px) {
    button {
      padding: 10px 9px;
      font-size: 1.1em;
    }
  }

  @media (max-width: 992px) {
    button {
      padding: 8px 6px;
      font-size: 1em;
    }
  }

</style>
