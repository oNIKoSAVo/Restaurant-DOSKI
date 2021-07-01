<script>
  import { franchiseRequest } from "./api";
  let name = "";
  let phone = "";

  function validate() {
    console.log("I'm the validate() function");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const response = await franchiseRequest({ name, phone });
    console.log(response);
  }
</script>

<form on:submit={handleSubmit} preventDefault={validate}>
  Имя<br />
  <input type="text" name="name" bind:value={name} /><br />
  Телефон<br />
  <input type="text" name="phone" bind:value={phone} /><br />
  <button>Отправить</button>
</form>

<style>
  .main {
  }
</style>
