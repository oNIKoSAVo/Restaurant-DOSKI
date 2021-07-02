<script>
  import { careerRequest } from "./api";

  let first_name = "";
  let middle_name = "";
  let last_name = "";
  let phone = "";
  let position = "";
  let city = "";
  let bar = "";
  let b_day = "";
  let citizenship = "";
  let about = "";

  function validate() {
    console.log("I'm the validate() function");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    b_day = b_day.split(".").reverse().join("-");
    const response = await careerRequest({
      first_name,
      middle_name,
      last_name,
      phone,
      position,
      city,
      bar,
      b_day,
      citizenship,
      about,
    });
    console.log(response);
  }
</script>

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
</form>

<style>
  .main {
  }
</style>
