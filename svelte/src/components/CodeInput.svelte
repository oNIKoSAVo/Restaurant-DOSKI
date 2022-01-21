<script>
  import isNumeric from "validator/es/lib/isNumeric";

  export let value;
</script>

<input
  class="code-input"
  on:input={(e) => {
    console.log(e.target.value.length);
    if (isNumeric(e.target.value, { no_symbols: true })) {
      if (e.target.value.length <= 1) {
        value = e.target.value;
      } else {
        e.target.value = e.target.value[0];
      }
    } else if (e.target.value === '') {
        value = e.target.value
    }
    else {
      e.target.value = value;
      console.log("blured");
    }
  }}
  {value}
/>
