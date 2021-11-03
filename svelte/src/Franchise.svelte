<script>
  import { franchiseRequest } from "./api";
  import isAlpha from "validator/es/lib/isAlpha";
  import isMobilePhone from "validator/es/lib/isMobilePhone";
  import Inputmask from "inputmask";
  import { correctPhoneWithMask } from "./helpers/correctPhoneWithMask";
  let name = "";
  let phone = "";
  let showModal = false;
  let isSent = false;
  let isError = false;

  function validate() {
    console.log("I'm the validate() function");
  }

  async function handleSubmit(e) {
    e.preventDefault();

    if (/*!isMobilePhone*/ !correctPhoneWithMask(phone)) {
      isError = true;
      showModal = true;
      return;
    }
    if (!isSent) {
      const response = await franchiseRequest({ name, phone });
      console.log(response);
      if (response.status === "success") {
        showModal = true;
        isSent = true;
        isError = false;
      }
    } else {
      showModal = true;
    }
  }
  document.addEventListener("DOMContentLoaded", function (event) {
    const selector = [
      ...document.querySelectorAll(".phone-input"),
      ...document.querySelectorAll("input[name=phone]"),
    ];
    const im = new Inputmask("+7(999)-999-99-99");
    selector.forEach((node) => {
      im.mask(node);
    });
    console.log({ selector });
  });
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
        value={name}
        on:input={(e) => {
          if (
            isAlpha(e.target.value, "ru-RU", { ignore: "s" }) ||
            e.target.value === ""
          )
            name = e.target.value;
          else e.target.value = name;
        }}
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
<div
  class="modal-wrapper modal fade {showModal ? 'show' : ''}"
  id="successFranchiseModal"
  tabindex="-1"
  role="dialog"
  style={showModal ? "display: block" : ""}
  on:click|stopPropagation={(e) => {
    if (e.target.classList.contains("modal-wrapper")) {
      showModal = false;
    }
  }}
>
  <div class="modal-dialog limited" style="max-width: 424px">
    <div class="modal-content">
      <button
        class="close"
        type="button"
        data-dismiss="modal"
        aria-label="Close"
      >
        <span aria-hidden="true">&times;</span>
      </button>
      <div class="modal-header mt-3">
        <div class="modal-title">
          {isError ? "Неверный номер" : "Ваша заявка успешно отправлена"}
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .main {
  }
</style>
