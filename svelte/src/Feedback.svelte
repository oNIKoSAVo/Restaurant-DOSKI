<script>
  import { feedbackRequest } from "./api";

  let name = "";
  let phone = "";
  let description = "";

  function validate() {
    console.log("I'm the validate() function");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const response = await feedbackRequest({ name, phone, description });
    console.log(response);
  }
</script>

<form on:submit={handleSubmit} preventDefault={validate}>
  Имя<br />
  <input type="text" name="name" bind:value={name} /><br />
  Телефон<br />
  <input type="text" name="phone" bind:value={phone} /><br />
  Сообщение<br />
  <textarea name="description" bind:value={description} /><br />
  <button>Отправить</button>
</form>

<style>
  .main {}
</style>
