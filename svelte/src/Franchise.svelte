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
  <div class="form-field">
    <div class="input-wrapper">
      <img src="/static/app/img/user.png" />
      <input
        class="input"
        required
        placeholder="Введите ваше ФИО"
        name="name"
        bind:value={name}
      />
    </div>
  </div>
  <div class="form-field">
    <div class="input-wrapper">
      <img src="/static/app/img/phone.png" />
      <input type="hidden" name="subject" value="Заказать звонок" />
      <input
        class="input phone-input"
        required
        name="phone"
        placeholder="Ваш телефон"
        bind:value={phone}
      />
    </div>
  </div>
  <input class="mt-3" type="submit" value="Оставьте заявку" />
</form>

<style>
  .main {
  }
</style>
