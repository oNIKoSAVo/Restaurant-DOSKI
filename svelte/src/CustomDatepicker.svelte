<script>
  import { Datepicker } from "svelte-calendar";
  import dayjs from "dayjs";
  import "dayjs/locale/ru.js";

  export let store;
  export let start;
  export let end;
  export let options;
  export let unselectedText;
  export let selected;
  export let automaticHasChosenOnDefault = true;
  let locale = "ru";
  $: dayjs.locale(locale);
  $: if (store && selected && automaticHasChosenOnDefault) {
    store.getState().hasChosen = true;
    console.log({ has: store.getState() });
  }
</script>

<Datepicker
  bind:selected
  on:mouseover={() => {
    document.body.classList.add("locked");
  }}
  {start}
  {end}
  bind:store
  let:key
  let:send
  let:receive
  startOfWeekIndex={1}
  theme={{
    calendar: {
      font: {
        large: "20em",
      },
    },
  }}
>
  <button
    style={`color: ${
      options?.color ?? "rgba(255, 255, 255, 0.7)"
    };max-width:128px`}
    id="chooseDate"
    type="button"
    class={options?.classList || ""}
    in:receive|local={{ key }}
    out:send|local={{ key }}
    on:click={() => {
      document
        .querySelectorAll(".sc-popover")
        .forEach((el) => (el.style.zIndex = 1000));
      document.body.classList.add("locked");
      document.onclick = (e) => {
        if (
          (e.target.closest(".sc-popover") &&
            !(e.target?.hash === "#pickday")) ||
          e.target.classList.contains("disabled")
        )
          return;
        document.body.classList.remove("locked");
        setTimeout(
          () =>
            document
              .querySelectorAll(".sc-popover")
              .forEach((el) => (el.style.zIndex = 1)),
          600
        );

        document.onclick = null;
      };
    }}
  >
    {#if $store?.hasChosen}
      <span style="color: black;">
        {dayjs($store.selected).format("ddd MMM D, YYYY")}</span
      >
    {:else}
      <span style="color: var(--secondary);"
        >{unselectedText || "Выберите дату"}</span
      >
    {/if}
  </button>
</Datepicker>

<style>

.Datepicker {
  min-width: 200px !important;
}

  button {
    background: transparent;
    border: 1px solid rgba(190, 190, 190, 0.5);
    padding: 18px 15px;

    font-size: 1.2em;
    border-radius: 6px;
    cursor: pointer;
    font-family: "Muller", sans-serif;
  }
</style>
